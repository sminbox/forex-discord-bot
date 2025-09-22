#!/usr/bin/env python3
"""
Forex Factory Calendar Discord Bot
Extracts daily forex events and posts to Discord with color coding
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import sys

def get_current_date_url():
    """Generate the current date URL for Forex Factory"""
    today = datetime.now()
    month_abbr = today.strftime("%b").lower()
    day = today.day
    year = today.year
    date_str = f"{month_abbr}{day:02d}.{year}"
    return f"https://www.forexfactory.com/calendar?day={date_str}"

def extract_forex_data_from_text(content):
    """Extract forex calendar data from scraped text content"""
    events = []
    lines = content.split('\n')
    
    # Look for table data in the scraped content
    in_table = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this looks like a table row with forex data
        if '|' in line and any(curr in line for curr in ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'NZD']):
            parts = [part.strip() for part in line.split('|')]
            if len(parts) >= 4:  # Time, Currency, Event, and other data
                try:
                    time = parts[0] if parts[0] and parts[0] != '-' else ""
                    currency = parts[1] if len(parts) > 1 else ""
                    event = parts[2] if len(parts) > 2 else ""
                    actual = parts[3] if len(parts) > 3 else "-"
                    forecast = parts[4] if len(parts) > 4 else "-"
                    previous = parts[5] if len(parts) > 5 else "-"
                    
                    # Skip header rows
                    if 'Time' in time or 'Currency' in currency or '---' in line:
                        continue
                    
                    # Determine impact level (simplified approach)
                    impact = "medium"  # Default to medium
                    if any(keyword in event.lower() for keyword in ['gdp', 'employment', 'inflation', 'interest rate', 'nfp']):
                        impact = "high"
                    elif any(keyword in event.lower() for keyword in ['speaks', 'speech', 'holiday']):
                        impact = "low"
                    
                    if time and currency and event:
                        events.append({
                            'time': time,
                            'currency': currency,
                            'event': event,
                            'impact': impact,
                            'actual': actual,
                            'forecast': forecast,
                            'previous': previous
                        })
                except:
                    continue
    
    return events

def extract_forex_data(url):
    """Extract forex calendar data from the website"""
    try:
        import subprocess
        import json
        
        # Call the scraper script
        result = subprocess.run([
            'python3', '/home/ubuntu/forex_scraper.py', url
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return None, f"Scraper failed: {result.stderr}"
        
        # Parse the JSON result
        data = json.loads(result.stdout)
        
        if "error" in data:
            return None, data["error"]
        
        return data.get("events", []), None
        
    except subprocess.TimeoutExpired:
        return None, "Scraping timeout"
    except json.JSONDecodeError as e:
        return None, f"JSON parsing error: {str(e)}"
    except Exception as e:
        return None, f"Error extracting data: {str(e)}"

def format_discord_message(events, date_str):
    """Format events for Discord with color coding"""
    if not events:
        return "No forex events found for today."
    
    # Process events to assign previous timestamp when missing
    processed_events = []
    last_time = ""
    
    for event in events:
        current_time = event['time'].strip() if event['time'] else ""
        
        # If no timestamp, use the last valid timestamp
        if not current_time or current_time == "":
            display_time = last_time
        else:
            display_time = current_time
            last_time = current_time  # Update last_time for next iteration
        
        processed_event = event.copy()
        processed_event['display_time'] = display_time
        processed_events.append(processed_event)
    
    # Format date for header (MM/DD/YYYY format)
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        formatted_date = date_obj.strftime("%m/%d/%Y")
    except:
        # Fallback to current date if parsing fails
        formatted_date = datetime.now().strftime("%m/%d/%Y")
    
    # Create message with News Events header
    message = f"🔔 **@everyone** 🔔\n\n"
    message += f"**📅 News Events: {formatted_date}**\n"
    message += "```\n"
    message += f"{'Time':<9} {'Curr':<4} {'Imp':<3} {'Event':<35} {'Actual':<8} {'Forecast':<8} {'Previous':<8}\n"
    message += "─" * 85 + "\n"
    
    for event in processed_events:
        # Color coding based on impact
        if event['impact'] == 'high':
            impact_symbol = "🔴"
        elif event['impact'] == 'medium':
            impact_symbol = "🟡"
        else:
            impact_symbol = "🟢"
        
        # Truncate event name if too long
        event_name = event['event'][:33] + ".." if len(event['event']) > 35 else event['event']
        
        message += f"{event['display_time']:<9} {event['currency']:<4} {impact_symbol:<3} {event_name:<35} {event['actual']:<8} {event['forecast']:<8} {event['previous']:<8}\n"
    
    message += "```\n"
    message += "\n🔴 High Impact  🟡 Medium Impact  🟢 Low Impact"
    
    return message

def send_to_discord(webhook_url, message):
    """Send message to Discord webhook"""
    data = {
        "content": message,
        "username": "Forex Calendar Bot"
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        return True, "Message sent successfully"
    except Exception as e:
        return False, f"Error sending to Discord: {str(e)}"

def main():
    """Main function"""
    import os
    
    # Get webhook URL from environment variable or use default
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL', 'https://discord.com/api/webhooks/1418165062643880027/kx7vkqsNJPYzfyHpgqoNA7yPXF3C3K7Acl5skRUJ3lkqlmNm5amMGQymIhKt3DVz8pq7')
    
    # Get current date URL
    url = get_current_date_url()
    date_str = datetime.now().strftime("%B %d, %Y")
    
    print(f"Extracting data from: {url}")
    
    # Extract forex data
    events, error = extract_forex_data(url)
    
    if error:
        error_message = f"❌ **Error extracting Forex data for {date_str}**\n{error}"
        send_to_discord(webhook_url, error_message)
        print(f"Error: {error}")
        return 1
    
    if not events:
        no_events_message = f"📅 **No Forex events scheduled for {date_str}**"
        send_to_discord(webhook_url, no_events_message)
        print("No events found")
        return 0
    
    # Format message
    message = format_discord_message(events, date_str)
    
    # Split message if too long (Discord limit is 2000 characters)
    if len(message) > 2000:
        # Send in parts
        parts = [message[i:i+1900] for i in range(0, len(message), 1900)]
        for i, part in enumerate(parts):
            if i == 0:
                part = f"🔔 **@everyone Forex Calendar - {date_str}** (Part {i+1}/{len(parts)}) 🔔\n\n" + part
            else:
                part = f"**Forex Calendar - {date_str}** (Part {i+1}/{len(parts)})\n\n" + part
            
            success, result = send_to_discord(webhook_url, part)
            if not success:
                print(f"Error sending part {i+1}: {result}")
                return 1
    else:
        success, result = send_to_discord(webhook_url, message)
        if not success:
            print(f"Error: {result}")
            return 1
    
    print(f"Successfully sent {len(events)} events to Discord")
    return 0

if __name__ == "__main__":
    sys.exit(main())
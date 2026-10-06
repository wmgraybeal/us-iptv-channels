#!/usr/bin/env python3
"""
Tiny IPTV Parser for 10-channel test dataset
"""

import csv
import sys
from pathlib import Path


def load_csv(csv_file):
    """Load and parse CSV file."""
    channels = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            channels.append(row)
    return channels


def load_m3u(m3u_file):
    """Load and parse M3U playlist."""
    channels = []
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF:"):
            name = "Unknown"
            group = "Other"
            
            if ',' in line:
                parts = line.split(',', 1)
                name = parts[1].strip()
                if 'group-title="' in parts[0]:
                    start = parts[0].find('group-title="') + 13
                    end = parts[0].find('"', start)
                    group = parts[0][start:end]
            
            url = ""
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith("#"):
                    url = next_line
                    i += 1
            
            if url:
                channels.append({
                    "channel_name": name,
                    "group": group,
                    "stream_url": url
                })
        i += 1
    
    return channels


def filter_by_group(channels, group):
    """Filter channels by group."""
    return [ch for ch in channels if ch.get('group', '').lower() == group.lower()]


def print_channels(channels):
    """Pretty print channels."""
    for ch in channels:
        print(f"  {ch['channel_name']:<20} | {ch['group']:<15} | {ch['stream_url']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python iptv_parser.py <file.csv|file.m3u> [--group GROUP]")
        print("\nExamples:")
        print("  python iptv_parser.py channels.csv")
        print("  python iptv_parser.py channels.m3u --group News")
        sys.exit(1)
    
    input_file = sys.argv[1]
    group_filter = None
    
    if "--group" in sys.argv:
        idx = sys.argv.index("--group")
        if idx + 1 < len(sys.argv):
            group_filter = sys.argv[idx + 1]
    
    if input_file.endswith('.csv'):
        channels = load_csv(input_file)
    elif input_file.endswith('.m3u'):
        channels = load_m3u(input_file)
    else:
        print("Error: File must be .csv or .m3u")
        sys.exit(1)
    
    if group_filter:
        channels = filter_by_group(channels, group_filter)
    
    print(f"\n📺 Channels ({len(channels)} total):")
    print_channels(channels)
    print()

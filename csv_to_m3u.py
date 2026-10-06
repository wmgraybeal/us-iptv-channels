#!/usr/bin/env python3
"""
Minimal CSV ↔ M3U Converter for IPTV Channels
"""

import csv
import sys
from pathlib import Path


def csv_to_m3u(csv_file, output_file=None):
    """Convert CSV to M3U playlist."""
    if output_file is None:
        output_file = Path(csv_file).stem + ".m3u"
    
    m3u_lines = ["#EXTM3U"]
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('channel_name', '').strip()
            group = row.get('group', '').strip()
            url = row.get('stream_url', '').strip()
            
            if name and url:
                extinf = f'#EXTINF:-1 tvg-id="{name.lower()}" tvg-name="{name}" group-title="{group}",{name}'
                m3u_lines.append(extinf)
                m3u_lines.append(url)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(m3u_lines))
    
    print(f"✓ Created: {output_file}")


def m3u_to_csv(m3u_file, output_file=None):
    """Convert M3U playlist to CSV."""
    if output_file is None:
        output_file = Path(m3u_file).stem + ".csv"
    
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
                    "source": group,
                    "stream_url": url,
                    "notes": "Imported from M3U"
                })
        
        i += 1
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["channel_name", "group", "source", "stream_url", "notes"])
        writer.writeheader()
        writer.writerows(channels)
    
    print(f"✓ Created: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_to_m3u.py <input.csv|input.m3u> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if input_file.endswith('.csv'):
        csv_to_m3u(input_file, output_file)
    elif input_file.endswith('.m3u'):
        m3u_to_csv(input_file, output_file)
    else:
        print("Error: File must be .csv or .m3u")
        sys.exit(1)

#!/usr/bin/env python3
"""Extract forward trades table from demandmanager.com.au"""

import re
import csv
import sys
from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td = False
        self.current_row = []
        self.rows = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
        elif tag == 'tr' and self.current_row:
            self.rows.append(self.current_row)
            self.current_row = []
            
    def handle_data(self, data):
        if self.in_td:
            self.current_row.append(data.strip())
            self.in_td = False

def main():
    html = sys.stdin.read()
    
    # Extract forward table HTML from JS
    match = re.search(r'forward_table_holder"\)\.html\(\'(.+?)\'\)', html)
    if not match:
        print("Could not find forward table data", file=sys.stderr)
        sys.exit(1)
    
    table_html = match.group(1).replace("\\'", "'")
    
    # Parse table
    parser = TableParser()
    parser.feed(table_html)
    if parser.current_row:
        parser.rows.append(parser.current_row)
    
    # Write CSV
    writer = csv.writer(sys.stdout)
    writer.writerow(['scheme', 'price', 'volume', 'trade_date', 'settlement_date'])
    for row in parser.rows:
        if len(row) == 5:
            row[1] = row[1].replace('$', '')
            writer.writerow(row)

if __name__ == "__main__":
    main()

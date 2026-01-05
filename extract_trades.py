#!/usr/bin/env python3
"""Extract spot and forward trades tables from demandmanager.com.au"""

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

def extract_table(html, holder_id):
    pattern = rf'{holder_id}"\)\.html\(\'(.+?)\'\)'
    match = re.search(pattern, html)
    if not match:
        return []
    
    table_html = match.group(1).replace("\\'", "'")
    parser = TableParser()
    parser.feed(table_html)
    if parser.current_row:
        parser.rows.append(parser.current_row)
    return parser.rows

def write_csv(rows, filename, headers, expected_cols):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            if len(row) == expected_cols:
                row[1] = row[1].replace('$', '')
                writer.writerow(row)

def main():
    html = sys.stdin.read()
    
    # Extract spot trades (4 columns)
    spot_rows = extract_table(html, 'spot_table_holder')
    write_csv(spot_rows, 'spot_trades.csv', 
              ['scheme', 'price', 'volume', 'date'], 4)
    
    # Extract forward trades (5 columns)
    forward_rows = extract_table(html, 'forward_table_holder')
    write_csv(forward_rows, 'forward_trades.csv',
              ['scheme', 'price', 'volume', 'trade_date', 'settlement_date'], 5)
    
    print(f"Extracted {len(spot_rows)} spot trades, {len(forward_rows)} forward trades")

if __name__ == "__main__":
    main()

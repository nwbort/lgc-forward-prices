#!/bin/bash
curl -s 'https://www.demandmanager.com.au/certificate-prices/' | python3 extract_forwards.py > forward_trades.csv

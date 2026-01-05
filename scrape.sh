#!/bin/bash
curl -s 'https://www.demandmanager.com.au/certificate-prices/' | python3 extract_trades.py

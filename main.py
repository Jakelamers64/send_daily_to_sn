#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# Add the script's directory to Python path (important for cron)
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from src.html_to_pdf import html_to_pdf
from src.send_pdf_to_sn import send_pdf_to_sn

def main():
    try:
        html_to_pdf()
        send_pdf_to_sn()
        os.remove(f"{datetime.today().strftime('%Y-%m-%d')}.pdf")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
if __name__ == "__main__":
    sys.exit(main())

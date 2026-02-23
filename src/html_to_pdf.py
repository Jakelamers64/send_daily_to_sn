import requests
import json

from weasyprint import HTML
from datetime import datetime

def get_calendar_html():
    """
    TODO
    """

    with open('config.json','r') as file:
        config = json.load(file)

    calendar_webpage_url = config["calendar_webpage_url"]

    response = requests.get(calendar_webpage_url)

    # Check if request was successful
    if response.status_code == 200:
        # Get the HTML content as text
        return response.text
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")



def html_to_pdf(body=""):
    """
    TODO
    """
    #Test Body should create dynamically
    body = "<html>"

    body += get_calendar_html()
    
    body += "</html>"

    HTML(string=body).write_pdf(f"{datetime.today().strftime('%Y-%m-%d')}.pdf")

from weasyprint import HTML

from datetime import datetime
from src.get_calendar_html import get_calendar_html

def html_to_pdf(body=""):
    """
    TODO
    """
    #Test Body should create dynamically
    body = "<html>"

    body += get_calendar_html()
    
    body += "</html>"

    HTML(string=body).write_pdf(f"{datetime.today().strftime('%Y-%m-%d')}.pdf")

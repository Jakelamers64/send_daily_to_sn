from weasyprint import HTML

from datetime import datetime

def html_to_pdf(body=""):
    """
    TODO
    """
    #Test Body should create dynamically
    body = """
    <html>
        <head></head>
        Hello World!
    </html>
    """

    HTML(string=body).write_pdf(f"{datetime.today().strftime('%Y-%m-%d')}.pdf")

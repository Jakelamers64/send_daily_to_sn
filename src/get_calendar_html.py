import math
import requests
import pytz

from datetime import datetime
from icalendar import Calendar
from tqdm import tqdm

def get_mcw_oasis_events_for_15_min_block(min_block):
  current_classes = [
      "INTE-12102", #Climb
      "PWAY-12210", #UCH
      "INTE-12104", #TGD
      "INTE-11106"  #Resp
  ]

  r = requests.get('https://oasis.acad.mcw.edu/calendar/m=9&m=29&m=3&m=5&m=11&m=23&m=24&m=25&m=26&m=28&m=12&m=16&m=27&m=8&m=6&m=30&m=14&m=10&m=4&module_name=Multiple%20Modules&export_to=gcal&export_length=7&yid=2026')

  calendar = Calendar.from_ical(r.text.encode('utf-8'))

  event_html = ""

  # Extract events
  for component in calendar.walk():
    if component.name == "VEVENT":

      if sum([current_class in str(component.get('description')) for current_class in current_classes]) > 0:
        event_date = component.get('dtstart').dt.replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=pytz.utc)
        today_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=pytz.utc)

        if event_date == today_date:
          start_time = component.get('dtstart').dt.replace(second=0, microsecond=0,tzinfo=pytz.timezone('America/Chicago'))
          end_time = component.get('dtend').dt.replace(second=0, microsecond=0,tzinfo=pytz.timezone('America/Chicago'))

          time_block_dt = datetime.today().replace(
              hour=int(min_block.split(':')[0]),
              minute=int(min_block.split(':')[1]),
              second=0,
              microsecond=0,
              tzinfo=pytz.timezone('America/Chicago')
          )

          #print(component.keys())

          if start_time <= time_block_dt and end_time > time_block_dt:
            event_html = event_html + "<div class='mcw-event-div'>" + str(component.get('summary')) + "<br>" + str(component.get('LOCATION')) + "<br>" + str(component.get('dtstart').dt) + "<br>" + str(component.get('dtend').dt) + "<br><br>" + "</div>"

  return event_html

def get_calendar_html():
    html_str = """
    <style>
        .schedule-table {
            border: 1px solid black;
            border-collapse: collapse;
            width: 100%;
        }
        .table-cell {
            border: 1px solid black;
            padding: 8px;
        }
        .time-cell {
            border: 1px solid black;
            padding: 8px;
            background-color: #f0f0f0;
            width: 1%;
            white-space: nowrap;
        }
        .schedule-cell {
            border: 1px solid black;
            padding: 8px;
            width: 1%;
            white-space: break-word;
            overflow-wrap: break-word;
            min-width: 60%;
        }
        .actual-cell {
            border: 1px solid black;
            padding: 8px;
        }
        .mcw-event-div {
            background-image:
                repeating-linear-gradient(
                    0deg,
                    rgba(0, 0, 0, 0.15),
                    rgba(0, 0, 0, 0.15)    2px,
                    rgba(255, 255, 255, 0) 2px,
                    rgba(255,255,255,0) 15px
                ),
                repeating-linear-gradient(
                    90deg,
                    rgba(0, 0, 0, 0.15),
                    rgba(0, 0, 0, 0.15)    2px,
                    rgba(255, 255, 255, 0) 2px,
                    rgba(255,255,255,0) 15px
                );
            background-repeat: no-repeat;
        }
    </style>
    <table class='schedule-table'>
    <tr>
        <td>Time</td>
        <td class='table-cell'>Schedule</td>
        <td class='table-cell'>Actual</td>
    </tr>
    """

    for i in tqdm(range(0,24*4)):
        html_str += "<tr>"
        html_str += "<td class='time-cell'>" + f"{math.floor(i/4)}:{(i%4)*15:02} - {math.floor((i+1)/4)}:{((i+1)%4)*15:02}" + "</td>"
        html_str += "<td class='schedule-cell'>" + get_mcw_oasis_events_for_15_min_block(f"{math.floor(i/4)}:{(i%4)*15:02}") + "</td>"
        html_str += "<td class='actual-cell'>"

    html_str += """
    </tr>
    </table>
    """

    return html_str

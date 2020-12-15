from PIL import Image, ImageDraw, ImageFont
import os

dirpath = os.path.dirname(os.path.realpath(__file__))

import pandas as pd
import pyodbc as db

import set_name as employ_name
Employee_name=employ_name.name()
# Employee_name = "Bashir Ahmed"
employee_search_name='%'+Employee_name+'%'
# print(employee_search_name)

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                   # give server name
                        'DATABASE=;'                 # give database name
                        'UID=;PWD=')                 # give id ans pass

cursor = connection.cursor()

employee_name_desig_df = pd.read_sql_query("""select asign_name,asign_designation,superviser_name from tasks
where asign_name like ?
and LEFT(format(cast(task_date as date),'yyyyMMdd'),6) =convert(varchar(6), GETDATE(),112)
and superviser_name is not null
group by asign_name,asign_designation,superviser_name """, connection,params={employee_search_name})


Asign_name = employee_name_desig_df['asign_name'].tolist()
designation = employee_name_desig_df['asign_designation'].tolist()
supervisor_name = employee_name_desig_df['superviser_name'].tolist()
Company_location = "Information System Automation (ERP)"
employee_information = [Asign_name[0],designation[0],Company_location,supervisor_name[0]]
print(employee_information)

# sys.exit()
from datetime import datetime

date = datetime.today()
months_first_day = str('01') + '/' + str(date.month) + '/' + str(date.year)
last_day = str(date.day-1) + '/' + str(date.month) + '/' + str(date.year)
print("months_first_day = ",months_first_day)
print("last_day = ",last_day)

import datetime
import calendar
def weekday_count(start, end):
  start_date  = datetime.datetime.strptime(start, '%d/%m/%Y')
  end_date    = datetime.datetime.strptime(end, '%d/%m/%Y')
  week        = {}
  for i in range((end_date - start_date).days):
    day       = calendar.day_name[(start_date + datetime.timedelta(days=i+1)).weekday()]
    week[day] = week[day] + 1 if day in week else 1
  return week

all_days_number=weekday_count(months_first_day,last_day)
print(all_days_number)

Fridays = all_days_number["Friday"]
Saturdays = all_days_number["Saturday"]

print("Fridays = ",Fridays)
print("Saturdays = ",Saturdays)

total_days_between_two_dates = date.day - 1
print("days_diff = ",total_days_between_two_dates)

target_hour= ((total_days_between_two_dates-Fridays-Saturdays)*8)+(Saturdays*4)
print("target_hour = ",target_hour)

Target_hour=str(target_hour)+"H"

employee_monthly_work_hour = pd.read_sql_query("""select left(sum(CAST((DATEDIFF(minute, start_time, end_time)) as  decimal(5, 2))/60),5) as work_time from tasks
where LEFT(format(cast(task_date as date),'yyyyMMdd'),6) =convert(varchar(6), GETDATE(),112)
and asign_name like ?""", connection,params={employee_search_name})

work_hour = employee_monthly_work_hour['work_time'].tolist()

Worked_hour=str(work_hour[0])+"H"


img = Image.open("./images/portfolio.png")

brand1_name = ImageDraw.Draw(img)

font1 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 62, encoding="unic")
font2 = ImageFont.truetype("./fonts/Anton-Regular.ttf", 20, encoding="unic")
font3 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 27, encoding="unic")
font4 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 20, encoding="unic")
font5 = ImageFont.truetype("./fonts/Anton-Regular.ttf", 25, encoding="unic")
font6 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 29, encoding="unic")
font7 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 23, encoding="unic")

brand1_name.text((272, 40), employee_information[0], (255,255,255), font=font1)
brand1_name.text((277, 123), employee_information[1], (255,255,255), font=font2)
brand1_name.text((277, 160), employee_information[2], (255,255,255), font=font3)
brand1_name.text((277, 230), "Supervised By:", (255,255,255), font=font5)
brand1_name.text((434, 230), employee_information[3], (253,208,59), font=font6)

brand1_name.text((1077, 100), "Target Hour:", (255,255,255), font=font4)
brand1_name.text((1077, 130), Target_hour, (253,208,59), font=font4)

brand1_name.text((1077, 180), "Worked Hour:", (255,255,255), font=font4)
brand1_name.text((1077, 210), Worked_hour, (253,208,59), font=font4)

brand1_name.text((840, 41), "Status:", (253,208,59), font=font7)

# brand1_name.text((960, 62), A[3], (0,0,0), font=font4)
# brand1_name.text((960, 125), A[4], (0,0,0), font=font4)

# profile_pic = Image.open("./images/bashir.png")
#
# imageSize = Image.new('RGB', (1270,1500 ))
# imageSize.paste(profile_pic, (50, 50))

img.save('./images/titles_marged.png')
print('name and information are merged with the picture.')
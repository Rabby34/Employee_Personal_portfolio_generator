import set_name
import title_writter
import achievement_circle_generator
# import yearly_contribution_circle
# import monthly_contribution_circle
import company_wise_hour
import day_wise_work_hour_bar
import company_wise_work_pie
import Category_wise_task
import leave_status
import sys


from PIL import Image, ImageDraw, ImageFont, ImageFilter

back = Image.open("./images/title_and_leave.png")
pro_pic = Image.open("./images/bashir.png")
achievement_hour_per = Image.open("./images/achievement_hour.png")
down_arrow = Image.open("./images/down_arrow.png")
up_arrow = Image.open("./images/up_arrow.png")
# yearly_contribution_donut=Image.open("./images/yearly_contribution.png")
# monthly_contribution_donut=Image.open("./images/monthly_contribution.png")
company_wise_bar = Image.open("./images/company_Wise_work_hour.png")
employee_daily_work_hour = Image.open("./images/Day_Wise_employee_work_hour.png")
company_wise_pie = Image.open("./images/company_wise_work_hour_pie.png")
category_wise_pie = Image.open("./images/category_wise_work_hour_pie.png")


import pandas as pd
import pyodbc as db

import set_name as employ_name
Employee_name=employ_name.name()
# Employee_name = "Bashir Ahmed"
# print(Employee_name)
# sys.exit()
employee_search_name='%'+Employee_name+'%'

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                   # give server name
                        'DATABASE=;'                 # give database name
                        'UID=;PWD=')                 # give id ans pass

cursor = connection.cursor()

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

Target_hour=float(target_hour)

employee_monthly_work_hour = pd.read_sql_query("""select left(sum(CAST((DATEDIFF(minute, start_time, end_time)) as  decimal(5, 2))/60),5) as work_time from tasks
where LEFT(format(cast(task_date as date),'yyyyMMdd'),6) =convert(varchar(6), GETDATE(),112)
and asign_name like ?""", connection,params={employee_search_name})

work_hour = employee_monthly_work_hour['work_time'].tolist()

Worked_hour=float(work_hour[0])
print("Worked hour = ",Worked_hour)

achievement = round((Worked_hour/Target_hour)*100,1)


imageSize = Image.new('RGB', (1270,1935))
imageSize.paste(back, (0, 0))
# imageSize.paste(pro_pic, (45, 59))
imageSize.paste(achievement_hour_per, (825, 66))
# imageSize.paste(yearly_contribution_donut, (35, 594))
# imageSize.paste(monthly_contribution_donut, (450, 594))
imageSize.paste(company_wise_bar, (25, 594))
imageSize.paste(employee_daily_work_hour, (15, 994))
imageSize.paste(company_wise_pie, (45, 1430))
imageSize.paste(category_wise_pie, (605, 1465))

if(achievement<=75):
    imageSize.paste(down_arrow, (1025, 140))
elif(achievement<=100):
    imageSize.paste(up_arrow, (1025, 140))



imageSize.save("./images/marge_all.png")

print("all are merged together.")

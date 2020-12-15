import matplotlib.pyplot as plt
import pandas as pd
import pyodbc as db

import set_name as employ_name
Employee_name=employ_name.name()

# Employee_name = "Bashir Ahmed"
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
# achievement = 85
if(achievement>100):
    data=[achievement-100, 100-(achievement-100)]
    colors = ['#128e18','#128e18']
    startangle=90
else:
    data = [achievement, 100-achievement]
    colors = ['#128e18', '#e5cf5b']
    startangle=90

if(achievement<=50):
    color1 = '#ff1a1a'
elif(achievement<=79):
    color1 = '#e5cf5b'
elif(achievement<=200):
    color1 = '#128e18'
# -----------------------------------------------------

fig1, ax = plt.subplots(figsize=(2.1,2.1),facecolor='#011936')
wedges, labels= ax.pie(data,radius=.06, colors=colors, startangle=startangle)
ax.text(0, -.006, str(round(achievement,1))+'%', ha='center', fontsize=25, fontweight='bold',color=color1)
#
centre_circle = plt.Circle((0, 0), 0.05, fc='#011936')

fig = plt.gcf()

fig.gca().add_artist(centre_circle)

# plt.title('Title of pie', fontsize=16, fontweight='bold', color='#ff6138')

ax.axis('equal')
plt.rcParams['savefig.facecolor'] = '#011936'
plt.tight_layout()
# plt.show()
plt.savefig('./images/achievement_hour.png', transparent=False)
print('work hour achieve circle generated')
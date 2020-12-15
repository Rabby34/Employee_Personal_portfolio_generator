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
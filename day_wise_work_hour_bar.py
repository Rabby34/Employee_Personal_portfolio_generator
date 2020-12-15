import os

dirpath = os.path.dirname(os.path.realpath(__file__))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyodbc as db

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                   # give server name
                        'DATABASE=;'                 # give database name
                        'UID=;PWD=')                 # give id ans pass

cursor = connection.cursor()

import set_name as employ_name
Employee_name=employ_name.name()

# Employee_name = "bashir ahmed"
employee_search_name='%'+Employee_name+'%'

daily_sales_df = pd.read_sql_query("""select right(format(cast(task_date as date),'yyyyMMdd'),2) as fixed_day,
isnull(left(sum(CAST((DATEDIFF(minute, start_time, end_time)) as  decimal(5, 2))/60),4),0) as work_time from tasks
where LEFT(format(cast(task_date as date),'yyyyMMdd'),6) =convert(varchar(6), GETDATE(),112)
and asign_name like ?
group by format(cast(task_date as date),'yyyyMMdd')
order by fixed_day""", connection,params={employee_search_name})


Every_day = daily_sales_df['fixed_day'].tolist()
print(Every_day)
y_pos = np.arange(len(Every_day))
print(y_pos)
every_day_work = daily_sales_df['work_time'].tolist()
print(every_day_work)
for i in range(0, len(every_day_work)):
    every_day_work[i] = float(every_day_work[i])
print(every_day_work)
x = np.arange(len(Every_day))

fig, ax = plt.subplots(figsize=(12.5, 4),facecolor='#011936')

# width = 0.35  # the width of the bars

rects2 = ax.bar(y_pos, every_day_work, label='Sales',color='#65B556')
# line = ax.plot(Target, color='green', label='Target')


# plt.yticks([])
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.set_xticks(x)
# ax.legend(fontsize=6,loc='upper right')
ax.set_xticklabels(Every_day,color='black')
ax.tick_params(axis='y', colors='white', labelsize=14)
ax.tick_params(axis='x', colors='white', labelsize=14)
ax.set_facecolor("#011936")


# plt.text(x[0], Target[0]+1000, format(Target[0], ',')+'K',fontsize=9,color='green', fontweight='bold')

def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                height,
                    ha='center', va='bottom',color='white', fontsize=12, rotation=0, fontweight='bold')

autolabel(rects2)
plt.rcParams['savefig.facecolor'] = '#011936'
fig.tight_layout()
# plt.show()
plt.savefig("./images/Day_Wise_employee_work_hour.png")
print('7. Day Wise Target vs Sales Generated')
#plt.close()
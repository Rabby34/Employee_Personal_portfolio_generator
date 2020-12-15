import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyodbc as db
import pandas as pd
import pyodbc as db

import set_name as employ_name
Employee_name=employ_name.name()

# Employee_name = "bashir ahmed"
employee_search_name='%'+Employee_name+'%'
# print(employee_search_name)

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                   # give server name
                        'DATABASE=;'                 # give database name
                        'UID=;PWD=')                 # give id ans pass

cursor = connection.cursor()

company_wise_hour_df = pd.read_sql_query("""select workfor_name,left(sum(CAST((DATEDIFF(minute, start_time, end_time)) as  decimal(5, 2))/60),5) as work_time from tasks
where LEFT(format(cast(task_date as date),'yyyyMMdd'),6) =convert(varchar(6), GETDATE(),112)
and workfor_name is not null
and asign_name like ?
group by workfor_name
order by work_time""", connection,params={employee_search_name})


Company_name = company_wise_hour_df['workfor_name'].tolist()
company=Company_name
work_hour_done = company_wise_hour_df['work_time'].tolist()
worked_hour=[]
print(company)
print(worked_hour)
for x in work_hour_done:
    new_value=float(x)
    worked_hour.append(new_value)
print(worked_hour)
fig, ax = plt.subplots(figsize=(8, 3.2),facecolor='#011936')

y_pos = np.arange(len(company))  # the label locations
width = 0.35  # the width of the bars
x = np.arange(len(company))
colors=['#008ac5','#72B41A','#E8C311','#F76300','#D8016C','#7F3B81']
rects2 = ax.bar(y_pos, worked_hour, width, label='Sales',color=colors)


# plt.yticks([])
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('white')
ax.set_xticks(x)
# ax.set_yticks(x)
# ax.legend(fontsize=6,loc='upper right')
ax.set_xticklabels(company,color='white')
ax.tick_params(axis='y', colors='white', labelsize=14)
ax.tick_params(axis='x', colors='white', labelsize=14)
ax.set_facecolor("#011936")


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
plt.savefig("./images/company_Wise_work_hour.png")
print('7. Day Wise Target vs Sales Generated')
#plt.close()
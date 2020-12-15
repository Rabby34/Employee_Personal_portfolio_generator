import matplotlib.pyplot as plt
import numpy as np
import pyodbc as db
import pandas as pd

colors = ['#008ac5','#72B41A','#E8C311','#F76300','#D8016C','#7F3B81']
#------------------------------------------------------
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

company_wise_hour_df = pd.read_sql_query("""select taskcategory_name,left(sum(CAST((DATEDIFF(minute, start_time, end_time)) as  decimal(5, 2))/60),5) as work_time from tasks
where LEFT(format(cast(task_date as date),'yyyyMMdd'),6) =convert(varchar(6), GETDATE(),112)
and taskcategory_name is not null
and asign_name like ?
group by taskcategory_name
order by work_time""", connection,params={employee_search_name})


Company_name = company_wise_hour_df['taskcategory_name'].tolist()
company=Company_name
work_hour_done = company_wise_hour_df['work_time'].tolist()
worked_hour=[]
print(company)
print(worked_hour)
for x in work_hour_done:
    new_value=float(x)
    worked_hour.append(new_value)
print(worked_hour)

labels = Company_name
data = worked_hour
total=sum(data)
print(total)
label_array_of_data=[]

for x in data:
    new_value=str(round((x/total)*100,1))+"%"
    label_array_of_data.append(new_value)
print(label_array_of_data)

fig1, ax1 = plt.subplots(figsize=(6.5,4.5),facecolor='#011936')
wedges,labelss=ax1.pie(data, labels=label_array_of_data,radius=.7,
 rotatelabels =True, labeldistance=.6,
    textprops = dict(rotation_mode = 'anchor', va='center', ha='left'),
        shadow=False, startangle=90)
plt.setp(labelss, **{'color':'white', 'weight':'bold', 'fontsize':11})
ax1.axis('equal')
# plt.legend(labels,loc='best',fontsize=9)
plt.legend(labels,loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
# bbox_props = dict(boxstyle="square,pad=0.3", fc="#DC3912", ec="k", lw=0.72)
# kw = dict(arrowprops=dict(arrowstyle="-",color='white'),
#           bbox=bbox_props, zorder=0, va="center")
#
# for i, p in enumerate(wedges):
#     ang = (p.theta2 - p.theta1)/2. + p.theta1
#     y = np.sin(np.deg2rad(ang))
#     x = np.cos(np.deg2rad(ang))
#     horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
#     connectionstyle = "angle,angleA=0,angleB={}".format(ang)
#     kw["arrowprops"].update({"connectionstyle": connectionstyle})
#     ax1.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),color='white',weight='bold',
#                 horizontalalignment=horizontalalignment, **kw)
# plt.title("Company Wise work hour",color='#E9C46A',fontsize=11,weight='bold')
plt.rcParams['savefig.facecolor'] = '#011936'
plt.tight_layout()
# plt.show()
plt.savefig('./images/category_wise_work_hour_pie.png', transparent=False)
print('Company wise task circle generated')
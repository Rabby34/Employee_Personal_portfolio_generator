from PIL import Image, ImageDraw, ImageFont

#yearly kpi, Monthly kpi
B=["80","70"]
import pandas as pd
import pyodbc as db
import sys

import set_name as employ_name
Employee_name=employ_name.name()

# Employee_name = "Bashir Ahmed"
employee_search_name='%'+Employee_name+'%'

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                   # give server name
                        'DATABASE=;'                 # give database name
                        'UID=;PWD=')                 # give id ans pass

employee_leave_status_df = pd.read_sql_query("""select 
         a.emp_name as 'Emp Name',
   
        
        a.PL as 'PL', a.CL as 'CL', a.SL as 'SL', a.TotalLeave as 'TL',
        b.Allocatedleave as 'AL'
        
       
                
        from (
        select payatd.emp_id, Emp_Info.emp_name,Emp_Info.designation,
        count(payatd.emp_id)-(count(case when atdstat = 'Absent' then atdstat end)+count(case when atdstat = 'CL' then atdstat end)+ count(case when atdstat = 'SL' then atdstat end)+ count(case when atdstat = 'PL' then atdstat end)) as 'StandardWorkingDay',
        count(case when atdstat = 'Absent' then atdstat end) as 'Absent',
        count(case when atdstat = 'PL' then atdstat end) as PL,
        count(case when atdstat = 'CL' then atdstat end) as CL,
        count(case when atdstat = 'SL' then atdstat end) as SL,
        count(case when atdstat = 'CL' then atdstat end)+ count(case when atdstat = 'SL' then atdstat end)+ count(case when atdstat = 'PL' then atdstat end) as 'TotalLeave',
        count(case when atdstat = 'CL' then atdstat end)+ count(case when atdstat = 'SL' then atdstat end) as 'LeaveWithoutPL',
        count(case when atdstat = 'Late' then atdstat end) as Late,
        count(case when atdstat = 'Present' then atdstat end) as Present,
        count(case when atdstat = 'Holiday' then atdstat end) as Holiday,
         CAST(phone_2 as int) as rank
        from payatd
        join Emp_Info
        on payatd.emp_id = Emp_Info.emp_id
        where year=Year(getdate()) and newid='erp' and status='active'
        group by payatd.emp_id, emp_name, designation, join_date, phone_2
        ) as a
        
        left join
        (select emp_id, cast(sum(total_leave) as int) as Allocatedleave from paylvbalance
        where iyear=Year(getdate())
        group by emp_id) as b
        on a.emp_id = b.emp_id
        where a.StandardWorkingDay>0 and a.rank >0
        and a.emp_name like ?
        order by a.rank asc, CEILING((a.TotalLeave*100)/b.Allocatedleave) desc
""", connection,params={employee_search_name})

employee_Alocated_leave=employee_leave_status_df["AL"].tolist()
employee_Total_leave=employee_leave_status_df["TL"].tolist()
employee_Sick_leave=employee_leave_status_df["SL"].tolist()
employee_Casual_leave=employee_leave_status_df["CL"].tolist()
employee_Privilage_leave=employee_leave_status_df["PL"].tolist()
# sys.exit()
img = Image.open("./images/titles_marged.png")

brand1_name = ImageDraw.Draw(img)

# font1 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 65, encoding="unic")
# font2 = ImageFont.truetype("./fonts/Anton-Regular.ttf", 20, encoding="unic")
font3 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 80, encoding="unic")
font4 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 55, encoding="unic")
font5 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 62, encoding="unic")
font6 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 27, encoding="unic")
font7 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 40, encoding="unic")
# font5 = ImageFont.truetype("./fonts/Anton-Regular.ttf", 25, encoding="unic")
# font6 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 29, encoding="unic")
# font7 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 23, encoding="unic")

brand1_name.text((890, 440), str(employee_Alocated_leave[0]), (25,131,118), font=font3)
brand1_name.text((1105, 440), str(employee_Total_leave[0]), (0,48,73), font=font3)
brand1_name.text((917, 592), str(employee_Sick_leave[0]), (214,40,40), font=font4)
brand1_name.text((1126, 592), str(employee_Casual_leave[0]), (227,100,20), font=font4)
brand1_name.text((915, 753), str(employee_Privilage_leave[0]), (58,12,163), font=font4)
brand1_name.text((1125, 753), '0', (40,54,24), font=font4)

brand1_name.text((40, 448), "unavailable", (255,255,255), font=font7)#62
brand1_name.text((455, 448), "unavailable", (255,255,255), font=font7)#62

import datetime
mydate = datetime.datetime.now()
month_name=mydate.strftime("%B")
print(month_name)

brand1_name.text((1097, 948),month_name, (249,215,59), font=font6)
# brand1_name.text((960, 62), A[3], (0,0,0), font=font4)
# brand1_name.text((960, 125), A[4], (0,0,0), font=font4)

# profile_pic = Image.open("./images/bashir.png")
#
# imageSize = Image.new('RGB', (1270,1500 ))
# imageSize.paste(profile_pic, (50, 50))

img.save('./images/title_and_leave.png')
print('name and information are merged with the picture.')
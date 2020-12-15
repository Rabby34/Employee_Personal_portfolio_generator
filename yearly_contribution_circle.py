import matplotlib.pyplot as plt

all_employee_hour = 20000
individual_hour = 2300

achievement = int((individual_hour/all_employee_hour)*100)

data = [achievement, 100-achievement]
colors = ['#00afb9', '#84dcc6']
startangle=90

color1 = '#16db93'
# -----------------------------------------------------

fig1, ax = plt.subplots(figsize=(3.1,3.1),facecolor='#011936')
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
plt.savefig('./images/yearly_contribution.png', transparent=False)
print('yearly contribution circle generated')
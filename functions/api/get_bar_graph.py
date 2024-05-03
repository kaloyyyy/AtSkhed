import sys
import os
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *
cursor.execute("SELECT gen, offsprings, fitness, conflicts, time FROM bargraph")

# Fetch all rows from the query result
rows = cursor.fetchall()

# Initialize lists to store data
generation = []
offsprings = []
f_score = []
conflict = []
time = []

# Iterate over the rows and extract data into lists
for row in rows:
    generation.append(row[0])
    offsprings.append(row[1])
    f_score.append(row['fitness'])
    conflict.append(row[3])
    time.append(row[4])

# Close the cursor and connection
cursor.close()
conn.close()

# Print the lists to verify the data
print("Generation:", generation)
print("Offsprings:", offsprings)
print("F-Score:", f_score)
print("Conflict:", conflict)
print("Time:", time)
fig = plt.figure(dpi=600)

ax = fig.add_subplot(111, projection='3d')

# Set dimensions of bars
legend_handles = []
legend_handles.append(mpatches.Patch(color='blue', label='16 offsprings'))
legend_handles.append(mpatches.Patch(color='red', label='32 offsprings'))
legend_handles.append(mpatches.Patch(color='cyan', label='40 offsprings'))
legend_handles.append(mpatches.Patch(color='green', label='48 offsprings'))
# Set dimensions of bars
previous=0
for x, x_size, y_size, z_size, offspring in zip(generation,f_score, time, conflict,offsprings):
    if offspring == 16:
        select_color = 'blue'

        gap = 0
    elif offspring == 32:
        select_color = 'red'

        gap = 2.5
    elif offspring == 40:
        select_color = 'cyan'

        gap = 5
    else:
        select_color = 'green'

        gap = 7.5

    ax.bar3d(x + gap,0 , 0, x_size, y_size, z_size, color=select_color, edgecolor='black', linewidth=0.1, antialiased=True, shade=True)

# Create 3D bars

ax.set_box_aspect([3.5,1.5,1])
# Set viewing angle
ax.set_xticks(range(0, max(generation) + 1, 10))
ax.set_xticklabels(range(0, max(generation) + 1, 10))
ax.view_init(azim=-80, elev=30)

# Set labels and title
# Add legend
plt.legend(handles=legend_handles)

ax.set_xlabel('Generation (x) | Fitness Score (width)')
ax.set_ylabel('Time\nSeconds)')
ax.set_zlabel('Conflict Count\n(Lower is better)')

plt.show()

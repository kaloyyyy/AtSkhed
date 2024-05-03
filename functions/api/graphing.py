import matplotlib.pyplot as plt
import numpy as np

# Given data
norm_fitness = [3.003458968, 8.329062862, 9.493335139, 9.633488309, 9.659666848, 9.682841384, 9.782139619, 9.69992048, 9.866866853]
generation = [0, 10, 20, 30, 40, 50, 60, 70, 80]
thickness_y = [239.25, 33.5625, 2.6875, 0.6875, 0.3125, 0.25, 0.0625, 0, 0]
norm_conflicts = [0.9563624249, 0.1341605596, 0.01074283811, 0.002748167888, 0.001249167222, 0.0009993337773, 0.0002498334443, 0, 0]
time = [62.9387, 159.2648, 164.2158, 180.0985, 172.2458, 184.0283, 218.9229, 268.3932, 290.4432]

# Create figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set dimensions of bars
# Set dimensions of bars

x_size = 8
y_size = time
z_size = norm_fitness

# Create 3D bars
for gen, y, z, z_size, x_size, y_size in zip(generation, thickness_y, np.zeros_like(generation), norm_conflicts, norm_fitness, time):
    ax.bar3d(gen, 0, 0, x_size, y_size, z_size, color='skyblue', edgecolor='black')

# Set viewing angle
ax.view_init(azim=-120, elev=30)

# Set labels and title
ax.set_xlabel('Generation (x) | Fitness Score (width)')
ax.set_ylabel('Time (seconds) (y)')
ax.set_zlabel('Conflict Count(z)\n(Lower is better)')
ax.set_title('Optimized 3D Bar Graph')

plt.show()

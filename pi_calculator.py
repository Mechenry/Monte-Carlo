"""
Last Version on Mon Sep 21 09:51:18 2020

@author: Henry K
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import random
from matplotlib.animation import FuncAnimation, PillowWriter

## Declare parameters
nominal_length = 1
frame_skip = 20  # Show every nth frame
interval = 2    # Time dedicated to each frame
num_points_to_graph = 1000   # Number of points to show on iterations graph
save_animation = False
iters = int(10e3)

fig = plt.figure(figsize=(15,11)) 
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

plt.sca(ax1)
# Square
p1 = [-nominal_length/2, -nominal_length/2]
p2 = [-nominal_length/2, nominal_length/2]
p3 = [nominal_length/2, nominal_length/2]
p4 = [nominal_length/2, -nominal_length/2]

plt.plot(p1,p2,'red')
plt.plot(p2,p3,'red')
plt.plot(p3,p4,'red')
plt.plot(p4,p1,'red')

# Circle
circle = plt.Circle((0, 0), nominal_length/2, fill=False, color='blue')

ax1.add_artist(circle)

square_hits = 0
circle_hits = 0
all_points = []
pi_calc = []

# Add random dots
for i in range(iters):
    x = random.uniform(-nominal_length/2,nominal_length/2)
    y = random.uniform(-nominal_length/2,nominal_length/2)
    
    all_points.append([x,y])
    # If the dot lands in the circle
    # If distance to centre is less than or equal to radius of circle
    if math.sqrt((x-0)**2 + (y-0)**2) <= nominal_length/2:
        circle_hits = circle_hits + 1
    # If the dot lands in the square
    else:
        square_hits = square_hits + 1
        
    if square_hits != 0:
        pi_calc.append((4*circle_hits/(square_hits+circle_hits)))
    else:
        pi_calc.append(0)

# Calculate Final Result
pi_calc_fin = 4*circle_hits/(square_hits+circle_hits)

## Determine Colours List
all_points = np.array(all_points)

circle_points = np.zeros([len(all_points), 2])
square_points = np.zeros([len(all_points), 2])
for i in range(iters):
    circle_points[i] = np.nan
    square_points[i] = np.nan
    if math.sqrt((all_points[i,0]-0)**2 + (all_points[i,1]-0)**2) <= nominal_length/2:
        circle_points[i] = all_points[i]
    else:
        square_points[i] = all_points[i]

circle_points = np.array(circle_points)
square_points = np.array(square_points)

graph1, = ax1.plot([], [], 'o', color = 'blue')
graph2, = ax1.plot([], [], 'o', color = 'red')
graph3, = ax2.plot([], [], lw=2, color='black', label='Monte Carlo Approximation')
graph4, = ax2.plot([], [], lw=2, color='red', label= r'True Value of $\pi$')

graph = [graph1, graph2, graph3, graph4]

ax2.grid()

def animate(i):
    # Plot circle and square
    plt.sca(ax1)
    graph[0].set_data(circle_points[:i+1,0],circle_points[:i+1,1])
    graph[1].set_data(square_points[:i+1,0],square_points[:i+1,1])
    plt.axis('equal')
    plt.axis('square')
    plt.xticks([])
    plt.yticks([])

    pi_calc_title = pi_calc[i]
    plt.title(r'$\pi \approx $'+ f"{pi_calc_title:.5f}",fontsize=17.5)

    plt.sca(ax2)
    if i < num_points_to_graph:
        y_min = min(pi_calc[0: i+1])
        y_max = max(pi_calc[0: i+1])
    else:
        y_min = min(pi_calc[i-num_points_to_graph:i+1])
        y_max = max(pi_calc[i-num_points_to_graph:i+1])
    
    if y_min > math.pi:
        y_min = math.pi
    if y_max < math.pi:
        y_max = math.pi
        
    y_range = y_max - y_min
    ax2.set_ylim(y_min-0.1*y_range, y_max+0.1*y_range)

    if i < num_points_to_graph:
        ax2.set_xlim(0, (i+1))
        graph[2].set_data(np.arange(i+1),pi_calc[:i+1])
    else:
        ax2.set_xlim(i-num_points_to_graph, (i+1))
        graph[2].set_data(np.arange(i-num_points_to_graph,i+1),\
                          pi_calc[i-num_points_to_graph:i+1])
        
    plt.xlabel('Iteration',fontsize=17.5)
    plt.ylabel(r'Value of $\pi$ Approximation',fontsize=17.5)
    ax2.legend(fontsize = 12, bbox_to_anchor=(1, 1.2), loc = 'outside right')
    # Plot real value of pi
    graph[3].set_data([0,len(pi_calc[:i])],[math.pi,math.pi])

    return graph
    
# ani = FuncAnimation(fig, animate, frames=int(iters), interval=2)
ani = FuncAnimation(fig, animate, frames=np.arange(1,iters,frame_skip), interval=interval)
if save_animation == True:
    writer = PillowWriter(fps=60)
    ani.save("Monte Carlo Pi.gif", writer=writer)

## Print Results
print("The Monte Carlo method has calculated; pi = %.5f" % (pi_calc_fin))
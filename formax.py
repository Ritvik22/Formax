import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import quad
from scipy.optimize import fsolve

# Function to compute the derivatives manually using finite difference approximation
def compute_derivatives(x, y, z_func):
    dzdx = (z_func(x + 1e-5, y) - z_func(x - 1e-5, y)) / (2 * 1e-5)
    dzdy = (z_func(x, y + 1e-5) - z_func(x, y - 1e-5)) / (2 * 1e-5)
    return dzdx, dzdy

# Define the arc length differential
def arc_length_integrand(x, y, z_func):
    dzdx, dzdy = compute_derivatives(x, y, z_func)
    return np.sqrt(1 + dzdx**2 + dzdy**2)

# Compute the arc length integrand along a given direction (theta) from (x0, y0)
def arc_length_direction(x0, y0, theta, s, z_func):
    x1 = x0 + s * np.cos(theta)
    y1 = y0 + s * np.sin(theta)
    return arc_length_integrand(x1, y1, z_func)

# Find the arc length from (x0, y0) along direction theta up to distance s
def compute_arc_length(x0, y0, theta, s, z_func):
    integrand = lambda s: arc_length_direction(x0, y0, theta, s, z_func)
    return quad(integrand, 0, s)[0]

# Given arc length l, find the corresponding s (distance) for a fixed theta
def find_s_for_arc_length(x0, y0, l, theta, z_func):
    s_solution = fsolve(lambda s: compute_arc_length(x0, y0, theta, s, z_func) - l, l)[0]
    return s_solution

# Function to compute angles and lengths from Cartesian points
def compute_angles_and_lengths(points_list):
    results = []
    for i in range(len(points_list)):
        x0, y0 = points_list[0]
        x1, y1 = points_list[i]
        dx = x1 - x0
        dy = y1 - y0
        theta = np.degrees(np.arctan2(dy, dx))
        s = np.sqrt(dx**2 + dy**2)
        results.append((x0, y0, theta, s))
    return results

# Example 3D function z = f(x, y)
def example_z_func(x, y, t=0):
    return 0.6 * np.sin(np.sqrt(x**2 + (y-4)**2) - 2 * t)

# Example list of Cartesian points
cartesian_points = [
    (0.0, 0.0),
    (0.0, 4.0),
    (0.0, 5.0),
    (-0.70711, 4.70711),
    (-1.51446, 4.45434),
    (-1.0, 4.0),
    (-2.0, 4.0),
    (-1.57329, 3.84267),
    (-2.8, 3.4),
    (-1.41421, 3.29289),
    (-0.70711, 3.29289),
    (-5.0, 3.0),
    (-3.87298, 3.0),
    (0.0, 3.0),
    (-2.19089, 2.90455),
    (-0.70711, 2.58579),
    (-1.41421, 2.58579),
    (-3.16228, 2.41886),
    (-2.12132, 1.87868),
    (-1.09545, 1.80911),
    (-0.34641, 1.57513),
    (-1.58114, 0.83772),
    (-0.5, 0.5),
    (0.0, 0.0),
]

# Animation setup
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121, projection='3d')

# Create an additional axis for the table
ax_table = fig.add_subplot(122)
ax_table.axis('off')

x_vals = np.linspace(-5.1, 0.1, 200)  # Increased resolution for smoothness
y_vals = np.linspace(-0.1, 5.1, 200)
X, Y = np.meshgrid(x_vals, y_vals)

def update(frame):
    ax.clear()
    Z = example_z_func(X, Y, t=frame * np.pi / 50)  # More frames for smooth animation
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')

    table_data = []
    for idx, (x0, y0, theta_deg, l) in enumerate(compute_angles_and_lengths(cartesian_points)):
        theta_rad = np.radians(theta_deg)
        s = find_s_for_arc_length(x0, y0, l, theta_rad, lambda x, y: example_z_func(x, y, t=frame * np.pi / 100))
        x1 = x0 + s * np.cos(theta_rad)
        y1 = y0 + s * np.sin(theta_rad)
        z1 = example_z_func(x1, y1, t=frame * np.pi / 50)
        ax.scatter([x1], [y1], [z1], color='red')
        ax.text(x1, y1, z1, f'{idx}', color='black')  # Label each point on the graph
        table_data.append([f"{idx}", f"{x1:.2f}", f"{y1:.2f}", f"{z1:.2f}"])

    # Set axis labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Frame {frame + 1}")  # Label each frame
    ax.view_init(elev=90, azim=-90)
    ax.set_zlim(-5, 5)

    # Update the table
    ax_table.clear()
    ax_table.axis('off')
    column_labels = ["Point Number", "X", "Y", "Z"]
    ax_table.table(cellText=table_data, colLabels=column_labels, loc='center', cellLoc='center')

# Create animation
ani = FuncAnimation(fig, update, frames=1, interval=50)  # More frames and shorter interval for smoothness

# Save animation as a gif
ani.save("Hand.gif", writer='pillow', fps=25)

plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import fsolve
import time  # Import the time module

# Function to compute the derivatives manually using finite difference approximation
def compute_derivatives(x, y, z_func):
    dzdx = (z_func(x + 1e-5, y) - z_func(x - 1e-5, y)) / (2 * 1e-5)
    dzdy = (z_func(x, y + 1e-5) - z_func(x, y - 1e-5)) / (2 * 1e-5)
    return dzdx, dzdy

# Define the arc length differential
def arc_length_integrand(x, y, z_func):
    dzdx, dzdy = compute_derivatives(x, y, z_func)
    return np.sqrt(1 + dzdx**2 + dzdy**2)

# Compute the arc length integrand along a given direction (theta) from (x0, y0)
def arc_length_direction(x0, y0, theta, s, z_func):
    x1 = x0 + s * np.cos(theta)
    y1 = y0 + s * np.sin(theta)
    return arc_length_integrand(x1, y1, z_func)

# Find the arc length from (x0, y0) along direction theta up to distance s
def compute_arc_length(x0, y0, theta, s, z_func):
    integrand = lambda s: arc_length_direction(x0, y0, theta, s, z_func)
    return quad(integrand, 0, s)[0]

# Given arc length l, find the corresponding s (distance) for a fixed theta
def find_s_for_arc_length(x0, y0, l, theta, z_func):
    s_solution = fsolve(lambda s: compute_arc_length(x0, y0, theta, s, z_func) - l, l)[0]
    return s_solution

# Function to compute angles and lengths from Cartesian points
def compute_angles_and_lengths(points_list):
    results = []
    for i in range(len(points_list)):
        x0, y0 = points_list[0]
        x1, y1 = points_list[i]
        dx = x1 - x0
        dy = y1 - y0
        theta = np.degrees(np.arctan2(dy, dx))
        s = np.sqrt(dx**2 + dy**2)
        results.append((x0, y0, theta, s))
    return results

# Function to plot points for a given 3D function z = f(x, y)
def plot_points_for_3d_function(points_list, z_func):
    # Prepare the 3D surface for plotting
    x_vals = np.linspace(-5, 5, 400)
    y_vals = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = z_func(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')

    # Loop through each point, compute theta and s, and plot the results
    for x0, y0, theta_deg, l in points_list:
        theta_rad = np.radians(theta_deg)  # Convert angle to radians
        s = find_s_for_arc_length(x0, y0, l, theta_rad, z_func)
        x1 = x0 + s * np.cos(theta_rad)
        y1 = y0 + s * np.sin(theta_rad)
        z1 = z_func(x1, y1)

        # Print the Cartesian coordinates
        print(f"Starting point: (x, y, z) = ({x0}, {y0}, {z_func(x0, y0)})")
        print(f"Point after arc length {l} at {theta_deg}°: (x, y, z) = ({x1}, {y1}, {z1})\n")

        # Plot the point on the surface
        ax.scatter([x1], [y1], [z1], s=100, label=f'Arc Length={l}, Angle={theta_deg}°')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=90, azim=-90)  # Set view perspective
    plt.show()
    
# Example 3D function z = f(x, y)

t = 0

def example_z_func(x, y):
    return (x**9+y**9)

# Example list of Cartesian points
cartesian_points = [
    (0.0, 0.0),
    #(0.0, 4.0),
    #(0.0, 5.0),
    #(-0.70711, 4.70711),
    #(-1.51446, 4.45434),
    #(-1.0, 4.0),
    #(-2.0, 4.0),
    #(-1.57329, 3.84267),
    #(-2.8, 3.4),
    #(-1.41421, 3.29289),
    #(-0.70711, 3.29289),
    #(-5.0, 3.0),
    #(-3.87298, 3.0),
    #(0.0, 3.0),
    #(-2.19089, 2.90455),
    #(-0.70711, 2.58579),
    #(-1.41421, 2.58579),
    #(-3.16228, 2.41886),
    #(-2.12132, 1.87868),
    #(-1.09545, 1.80911),
    #(-0.34641, 1.57513),
    #(-1.58114, 0.83772),
    #(-0.5, 0.5),
    #(0.0, 0.0),
    (3.0, 4.0),
    (0, 5.0),
    
    
]


    # Compute angles and lengths from Cartesian points
points_with_angles_and_lengths = compute_angles_and_lengths(cartesian_points)

    # Plot the points on the 3D surface
plot_points_for_3d_function(points_with_angles_and_lengths, example_z_func)



import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import fsolve
import time  # Import the time module
from sympy import symbols, sin, sqrt, diff, lambdify

# Define symbolic variables
x, y = symbols('x y')

# Define the symbolic function z = f(x, y)
z_sym = sin(sqrt(x**2 + y**2))  # Use SymPy's sin and sqrt functions

# Compute symbolic derivatives
dzdx_sym = diff(z_sym, x)
dzdy_sym = diff(z_sym, y)

# Convert symbolic expressions to callable functions
z_func = lambdify((x, y), z_sym, 'numpy')  # Converts symbolic z to a NumPy-compatible function
dzdx_func = lambdify((x, y), dzdx_sym, 'numpy')  # Converts dz/dx to NumPy-compatible function
dzdy_func = lambdify((x, y), dzdy_sym, 'numpy')  # Converts dz/dy to NumPy-compatible function

# Function to compute the derivatives analytically
def compute_derivatives(x_val, y_val):
    dzdx = dzdx_func(x_val, y_val)
    dzdy = dzdy_func(x_val, y_val)
    return dzdx, dzdy

# Define the arc length differential
def arc_length_integrand(x_val, y_val):
    dzdx, dzdy = compute_derivatives(x_val, y_val)
    return np.sqrt(1 + dzdx**2 + dzdy**2)

# Compute the arc length integrand along a given direction (theta) from (x0, y0)
def arc_length_direction(x0, y0, theta, s):
    x1 = x0 + s * np.cos(theta)
    y1 = y0 + s * np.sin(theta)
    return arc_length_integrand(x1, y1)

# Find the arc length from (x0, y0) along direction theta up to distance s
def compute_arc_length(x0, y0, theta, s):
    integrand = lambda s: arc_length_direction(x0, y0, theta, s)
    return quad(integrand, 0, s)[0]

# Given arc length l, find the corresponding s (distance) for a fixed theta
def find_s_for_arc_length(x0, y0, l, theta):
    s_solution = fsolve(lambda s: compute_arc_length(x0, y0, theta, s) - l, l)[0]
    return s_solution

# Function to compute angles and lengths from Cartesian points
def compute_angles_and_lengths(points_list):
    results = []
    for i in range(len(points_list)):
        x0, y0 = points_list[0]
        x1, y1 = points_list[i]
        dx = x1 - x0
        dy = y1 - y0
        theta = np.degrees(np.arctan2(dy, dx))
        s = np.sqrt(dx**2 + dy**2)
        results.append((x0, y0, theta, s))
    return results

# Function to plot points for a given 3D function z = f(x, y)
def plot_points_for_3d_function(points_list):
    # Prepare the 3D surface for plotting
    x_vals = np.linspace(-5, 5, 400)
    y_vals = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = z_func(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')

    # Loop through each point, compute theta and s, and plot the results
    for x0, y0, theta_deg, l in points_list:
        theta_rad = np.radians(theta_deg)  # Convert angle to radians
        s = find_s_for_arc_length(x0, y0, l, theta_rad)
        x1 = x0 + s * np.cos(theta_rad)
        y1 = y0 + s * np.sin(theta_rad)
        z1 = z_func(x1, y1)

        # Print the Cartesian coordinates
        print(f"Starting point: (x, y, z) = ({x0}, {y0}, {z_func(x0, y0)})")
        print(f"Point after arc length {l} at {theta_deg}°: (x, y, z) = ({x1}, {y1}, {z1})\n")

        # Plot the point on the surface
        ax.scatter([x1], [y1], [z1], s=100, label=f'Arc Length={l}, Angle={theta_deg}°')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=20, azim=20)  # Set view perspective
    plt.legend()
    plt.show()

# Example list of Cartesian points
cartesian_points = [
    (0.0, 4.0),
    (0.0, 5.0),
    (-0.70711, 4.70711),
    (-1.51446, 4.45434),
    (-1.0, 4.0),
    (-2.0, 4.0),
    (-1.57329, 3.84267),
    (-2.8, 3.4),
    (-1.41421, 3.29289),
    (-0.70711, 3.29289),
    (-5.0, 3.0),
    (-3.87298, 3.0),
    (0.0, 3.0),
    (-2.19089, 2.90455),
    (-0.70711, 2.58579),
    (-1.41421, 2.58579),
    (-3.16228, 2.41886),
    (-2.12132, 1.87868),
    (-1.09545, 1.80911),
    (-0.34641, 1.57513),
    (-1.58114, 0.83772),
    (-0.5, 0.5),
    (0.0, 0.0),
]

# Start the timer
start_time = time.time()

for i in range(500):
    # Compute angles and lengths from Cartesian points
    points_with_angles_and_lengths = compute_angles_and_lengths(cartesian_points)

    # Plot the points on the 3D surface
    plot_points_for_3d_function(points_with_angles_and_lengths)

# End the timer
end_time = time.time()

# Calculate the total time
total_time = end_time - start_time
print(f"Total time for execution: {total_time:.2f} seconds")


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import quad
from scipy.optimize import fsolve

# Function to compute the derivatives manually using finite difference approximation
def compute_derivatives(x, y, z_func):
    dzdx = (z_func(x + 1e-5, y) - z_func(x - 1e-5, y)) / (2 * 1e-5)
    dzdy = (z_func(x, y + 1e-5) - z_func(x, y - 1e-5)) / (2 * 1e-5)
    return dzdx, dzdy

# Define the arc length differential
def arc_length_integrand(x, y, z_func):
    dzdx, dzdy = compute_derivatives(x, y, z_func)
    return np.sqrt(1 + dzdx**2 + dzdy**2)

# Compute the arc length integrand along a given direction (theta) from (x0, y0)
def arc_length_direction(x0, y0, theta, s, z_func):
    x1 = x0 + s * np.cos(theta)
    y1 = y0 + s * np.sin(theta)
    return arc_length_integrand(x1, y1, z_func)

# Find the arc length from (x0, y0) along direction theta up to distance s
def compute_arc_length(x0, y0, theta, s, z_func):
    integrand = lambda s: arc_length_direction(x0, y0, theta, s, z_func)
    return quad(integrand, 0, s)[0]

# Given arc length l, find the corresponding s (distance) for a fixed theta
def find_s_for_arc_length(x0, y0, l, theta, z_func):
    s_solution = fsolve(lambda s: compute_arc_length(x0, y0, theta, s, z_func) - l, l)[0]
    return s_solution

# Function to compute angles and lengths from Cartesian points
def compute_angles_and_lengths(points_list):
    results = []
    for i in range(len(points_list)):
        x0, y0 = points_list[0]
        x1, y1 = points_list[i]
        dx = x1 - x0
        dy = y1 - y0
        theta = np.degrees(np.arctan2(dy, dx))
        s = np.sqrt(dx**2 + dy**2)
        results.append((x0, y0, theta, s))
    return results

# Example 3D function z = f(x, y)
def example_z_func(x, y, t=0):
    return 0.6 * np.sin(np.sqrt(x**2 + (y-4)**2) - 2 * t)

# Example list of Cartesian points
cartesian_points = [
    (0.0, 4.0),
    (0.0, 5.0),
    (-0.70711, 4.70711),
    (-1.51446, 4.45434),
    (-1.0, 4.0),
    (-2.0, 4.0),
    (-1.57329, 3.84267),
    (-2.8, 3.4),
    (-1.41421, 3.29289),
    (-0.70711, 3.29289),
    (-5.0, 3.0),
    (-3.87298, 3.0),
    (0.0, 3.0),
    (-2.19089, 2.90455),
    (-0.70711, 2.58579),
    (-1.41421, 2.58579),
    (-3.16228, 2.41886),
    (-2.12132, 1.87868),
    (-1.09545, 1.80911),
    (-0.34641, 1.57513),
    (-1.58114, 0.83772),
    (-0.5, 0.5),
    (0.0, 0.0),
]

# Animation setup
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121, projection='3d')

# Create an additional axis for the table
ax_table = fig.add_subplot(122)
ax_table.axis('off')

x_vals = np.linspace(-5.1, 0.1, 200)  # Increased resolution for smoothness
y_vals = np.linspace(-0.1, 5.1, 200)
X, Y = np.meshgrid(x_vals, y_vals)

# List to store positions of point 10 over frames
point_10_positions = []

def update(frame):
    ax.clear()
    Z = example_z_func(X, Y, t=frame * np.pi / 50)  # More frames for smooth animation
    ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')

    table_data = []
    for idx, (x0, y0, theta_deg, l) in enumerate(compute_angles_and_lengths(cartesian_points)):
        theta_rad = np.radians(theta_deg)
        s = find_s_for_arc_length(x0, y0, l, theta_rad, lambda x, y: example_z_func(x, y, t=frame * np.pi / 100))
        x1 = x0 + s * np.cos(theta_rad)
        y1 = y0 + s * np.sin(theta_rad)
        z1 = example_z_func(x1, y1, t=frame * np.pi / 50)
        ax.scatter([x1], [y1], [z1], color='red')
        table_data.append([f"{idx}", f"{x1:.2f}", f"{y1:.2f}", f"{z1:.2f}"])

        # Record position of point 10
        if idx == 9:  # Point 10 is at index 9
            point_10_positions.append([x1, y1, z1])

    # Set axis labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Frame {frame + 1}")  # Label each frame
    ax.view_init(elev=90, azim=-90)  # Bird's-eye view (top-down view)
    ax.set_zlim(-5, 5)

    # Update the table
    ax_table.clear()
    ax_table.axis('off')
    column_labels = ["Point Number", "X", "Y", "Z"]
    ax_table.table(cellText=table_data, colLabels=column_labels, loc='center', cellLoc='center')

# Create animation
ani = FuncAnimation(fig, update, frames=50, interval=50)  # Record for the first 50 frames

# Save animation as a gif
ani.save("PleaseJustWork2.gif", writer='pillow', fps=25)

# Plot recorded positions of point 10 (Bird's-eye View)
# Plot recorded positions of point 10 (Bird's-eye View)
point_10_positions = np.array(point_10_positions)
fig_2 = plt.figure(figsize=(12, 6))
ax_2 = fig_2.add_subplot(111, projection='3d')

# Plot the trajectory of point 10
ax_2.plot3D(point_10_positions[:, 0], point_10_positions[:, 1], point_10_positions[:, 2], 'blue', label='Point 10')

# Add arrows to show progression from frame 1 to frame 50
for i in range(1, len(point_10_positions)-1, 5):  # Skip some frames to reduce arrows
    # Calculate direction from the previous point to the next
    dx = point_10_positions[i, 0] - point_10_positions[i-1, 0]
    dy = point_10_positions[i, 1] - point_10_positions[i-1, 1]
    dz = point_10_positions[i, 2] - point_10_positions[i-1, 2]
    
    # Make sure that the arrows are not too small at the ends
    if np.linalg.norm([dx, dy, dz]) > 0.1:  # Avoid drawing too small arrows
        ax_2.quiver(point_10_positions[i, 0], point_10_positions[i, 1], point_10_positions[i, 2],
                    dx, dy, dz, color='red', length=0.1, normalize=True)  # Adjust arrow size

# Set bird's-eye view (top-down)
ax_2.view_init(elev=90, azim=-45)  # Top-down view

# Labels and title
ax_2.set_xlabel('X')
ax_2.set_ylabel('Y')
ax_2.set_zlabel('Z')
ax_2.set_title("Movement of Point 10 Over Frames (Bird's-eye View)")

plt.show()

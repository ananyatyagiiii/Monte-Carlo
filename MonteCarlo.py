import numpy as np

# How many random darts to throw
n_samples = 1000

# Step 1: Generate random (x, y) coordinates
# The square goes from -1 to 1 in both directions
x = np.random.uniform(-1, 1, n_samples)
y = np.random.uniform(-1, 1, n_samples)

# Step 2: Calculate distance from origin (0, 0) for each point
# A point is inside the circle (radius 1) if distance <= 1
distances = np.sqrt(x**2 + y**2)

# Step 3: Count how many points landed inside the circle
inside_circle = np.sum(distances <= 1)

# Step 4: Calculate π
# Ratio of areas: inside_circle / total = π/4
# So: π = 4 * (inside_circle / total)
pi_estimate = 4 * inside_circle / n_samples

print(f"Estimated π: {pi_estimate:.6f}")
print(f"Actual π:    {np.pi:.6f}")
print(f"Error:       {abs(pi_estimate - np.pi):.6f}")


#Visualisation of the points
#import matplotlib.pyplot as plt
#inside_mask=distances<=1
#plt.figure(figsize=(8,8))
#plt.scatter(x[inside_mask], y[inside_mask], c='blue', s=1, alpha=0.5, label='Inside Circle')
#plt.scatter(x[~inside_mask], y[~inside_mask], c='red', s=1, alpha=0.5, label='Outside circle') #~ means NOT, so this refers to the points outside the circle
#circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
#plt.gca().add_patch(circle)
#plt.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'k-', linewidth=2)
#plt.xlim(-1.2, 1.2)
#plt.ylim(-1.2, 1.2)
#plt.gca().set_aspect('equal')
#plt.legend()
#plt.title(f'Monte Carlo π Estimation\nEstimate: {pi_estimate:.4f}, Actual: {np.pi:.4f}')
#plt.show()

import matplotlib.pyplot as plt

# Try different numbers of samples
sample_sizes = [100, 500, 1000, 5000, 10000]
estimates = []

for n_samples in sample_sizes:
    x = np.random.uniform(-1, 1, n_samples)
    y = np.random.uniform(-1, 1, n_samples)
    distances = np.sqrt(x**2 + y**2)
    inside_circle = np.sum(distances <= 1)
    pi_estimate = 4 * inside_circle / n_samples
    estimates.append(pi_estimate)
    print(f"Samples: {n_samples:>5} → Estimate: {pi_estimate:.6f}, Error: {abs(pi_estimate - np.pi):.6f}")

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(sample_sizes, estimates, 'o-', linewidth=2, markersize=8, label='MC estimate')
plt.axhline(np.pi, color='red', linestyle='--', linewidth=2, label='Actual π')
plt.xlabel('Number of Samples')
plt.ylabel('π Estimate')
plt.title('Monte Carlo Convergence: More Samples = Better Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
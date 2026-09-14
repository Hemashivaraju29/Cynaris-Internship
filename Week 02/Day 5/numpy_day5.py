# NumPy Fundamentals & Performance - Week 2 Day 5

import numpy as np
import time

# --------------------------------------------------
# 1. CREATE AND MANIPULATE 1D, 2D AND 3D ARRAYS
# --------------------------------------------------

# 1D array
array_1d = np.array([10, 20, 30, 40, 50])

# 2D array
array_2d = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

# 3D array
array_3d = np.array([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])

print("========== 1D ARRAY ==========")
print(array_1d)
print("Shape:", array_1d.shape)

print("\n========== 2D ARRAY ==========")
print(array_2d)
print("Shape:", array_2d.shape)

print("\n========== 3D ARRAY ==========")
print(array_3d)
print("Shape:", array_3d.shape)

# Array manipulation
reshaped_array = np.arange(1, 13).reshape(3, 4)

print("\n========== RESHAPED ARRAY ==========")
print(reshaped_array)

# --------------------------------------------------
# 2. VECTORIZED OPERATIONS
# --------------------------------------------------

numbers = np.array([1, 2, 3, 4, 5])

print("\n========== VECTORIZED OPERATIONS ==========")

print("Original:", numbers)
print("Add 10:", numbers + 10)
print("Multiply by 2:", numbers * 2)
print("Square:", numbers ** 2)

# 2D vectorized operations
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print("\nMatrix:")
print(matrix)

print("\nSum of all values:", np.sum(matrix))
print("Sum across rows:", np.sum(matrix, axis=1))
print("Sum across columns:", np.sum(matrix, axis=0))
print("Mean of all values:", np.mean(matrix))

# --------------------------------------------------
# 3. BOOLEAN MASKING AND FANCY INDEXING
# --------------------------------------------------

data = np.array([10, 25, 30, 45, 50, 65, 70])

print("\n========== BOOLEAN MASKING ==========")

# Select values greater than 40
mask = data > 40
print("Values greater than 40:", data[mask])

# Select even values
even_values = data[data % 2 == 0]
print("Even values:", even_values)

print("\n========== FANCY INDEXING ==========")

# Select specific positions
selected_values = data[[0, 2, 5]]
print("Values at indexes 0, 2 and 5:", selected_values)

# --------------------------------------------------
# 4. STATISTICAL MEASURES
# --------------------------------------------------

statistics_data = np.array([
    10, 20, 30, 40, 50,
    60, 70, 80, 90, 100
])

print("\n========== STATISTICAL MEASURES ==========")

mean_value = np.mean(statistics_data)
std_value = np.std(statistics_data)
percentile_50 = np.percentile(statistics_data, 50)
percentile_90 = np.percentile(statistics_data, 90)

print("Mean:", mean_value)
print("Standard deviation:", std_value)
print("50th percentile:", percentile_50)
print("90th percentile:", percentile_90)

# Correlation
x = np.array([10, 20, 30, 40, 50])
y = np.array([20, 40, 60, 80, 100])

correlation_matrix = np.corrcoef(x, y)

print("\nCorrelation matrix:")
print(correlation_matrix)

print("Correlation between x and y:", correlation_matrix[0, 1])

# --------------------------------------------------
# 5. NUMPY PERFORMANCE VS PYTHON LOOP
# --------------------------------------------------

print("\n========== PERFORMANCE COMPARISON ==========")

# Create 1 million values
large_data = np.arange(1_000_000)

# Python loop
start_time = time.perf_counter()

loop_result = [value * 2 for value in large_data]

loop_time = time.perf_counter() - start_time

# NumPy vectorized operation
start_time = time.perf_counter()

numpy_result = large_data * 2

numpy_time = time.perf_counter() - start_time

print("Number of values:", len(large_data))
print(f"Python loop time: {loop_time:.6f} seconds")
print(f"NumPy vectorized time: {numpy_time:.6f} seconds")

if numpy_time > 0:
    speedup = loop_time / numpy_time
    print(f"NumPy speedup: {speedup:.2f}x faster")

# Verify both methods produce the same result
print(
    "Results match:",
    np.array_equal(np.array(loop_result), numpy_result)
)

print("\n========== NUMPY DAY 5 COMPLETED ==========")
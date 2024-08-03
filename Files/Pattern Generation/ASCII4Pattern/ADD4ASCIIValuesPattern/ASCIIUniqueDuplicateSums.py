from itertools import product
import collections

# Define the number ranges
ranges = [
        range(0, 256),
        range(256, 512),
        range(512, 768),
        range(768, 1024)
]

# Dictionary to store sum counts
sum_counts = collections.Counter()

# Generate all permutations and count sums
total_permutations = 0
for perm in product(*ranges):
    perm_sum = sum(perm)
    sum_counts[perm_sum] += 1
    total_permutations += 1

# Calculate unique sums and duplicates
unique_sums = len(sum_counts)
duplicates = sum(value > 1 for value in sum_counts.values())

# Display results
print(f"Total permutations: {total_permutations}")
print(f"Total unique sums: {unique_sums}")
print(f"Total duplicate sums: {duplicates}")

# Display a sample of sum counts
sample_sums = list(sum_counts.items())[:10]
print("Sample of sums and their counts:")
for perm_sum, count in sample_sums:
    print(f"Sum: {perm_sum}, Count: {count}")

import os
import json
from itertools import product
import collections

# Define the ranges
ranges = [
    range(0, 256),
    range(256, 512),
    range(512, 768),
    range(768, 1024)
]

# Parameters
start_index = 0  # Adjust as needed
end_index = 10000  # Adjust as needed
num_files_in_batch = 10  # Adjust as needed
lines_per_file = 1000  # Adjust as needed
output_dir = "output"  # Adjust as needed

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize dictionary to store sum counts
sum_counts = collections.Counter()

# Generate all permutations and count sums
total_permutations = 0
all_permutations = list(product(*ranges))[start_index:end_index]
for perm in all_permutations:
    perm_sum = sum(perm)
    sum_counts[perm_sum] += 1
    total_permutations += 1

# Find duplicate sums and create unique mapping
unique_sum_map = {}
next_unique_sum = 2561  # Starting point for unique sums for duplicates

for perm_sum, count in sum_counts.items():
    if count > 1:
        for _ in range(count):
            unique_sum_map[(perm_sum, _)] = next_unique_sum
            next_unique_sum += 1

# Second pass: generate permutations and apply unique mapping
permutations_with_unique_sums = []
duplicate_tracker = collections.defaultdict(int)

for perm in all_permutations:
    perm_sum = sum(perm)
    if sum_counts[perm_sum] > 1:
        unique_sum = unique_sum_map[(perm_sum, duplicate_tracker[perm_sum])]
        duplicate_tracker[perm_sum] += 1
    else:
        unique_sum = perm_sum

    permutations_with_unique_sums.append({"permutation": perm, "unique_sum": unique_sum})

# Split into multiple files as needed
def write_to_file(data_batch, file_index):
    file_path = os.path.join(output_dir, f"data_part_{file_index}.json")
    with open(file_path, 'w') as file:
        json.dump(data_batch, file, indent=4)

# Write the data to multiple files
batch = []
file_index = 1

for item in permutations_with_unique_sums:
    batch.append(item)
    if len(batch) == lines_per_file:
        write_to_file(batch, file_index)
        batch = []
        file_index += 1
        if file_index > num_files_in_batch:
            break

# Write any remaining data
if batch and file_index <= num_files_in_batch:
    write_to_file(batch, file_index)

# Display results
unique_sums = len(sum_counts)
duplicates = sum(value > 1 for value in sum_counts.values())

print(f"Total permutations processed: {total_permutations}")
print(f"Total unique sums: {unique_sums}")
print(f"Total duplicate sums: {duplicates}")
print(f"Files generated: {file_index}")

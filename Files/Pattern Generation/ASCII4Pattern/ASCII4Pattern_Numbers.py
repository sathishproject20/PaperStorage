import json
from itertools import product, islice
import os

# Parameters
lines_per_file = 1000        # Number of lines per file
num_files_in_batch = 10       # Number of files per batch
output_dir = "output"        # Output directory
start_index = 0             # Start index for permutations
end_index = 10000           # End index for permutations (None for no limit)

# Define the number ranges based on i_values
i_values = [256, 256, 256, 256]
ranges = [range(0, i) for i in i_values]

# Calculate total permutations
total_permutations = 1
for i in i_values:
    total_permutations *= i
print(f"Total permutations: {total_permutations}")

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to write a batch of data to a file
def write_to_file(data_batch, file_index):
    file_path = os.path.join(output_dir, f"data_part_{file_index}.json")
    try:
        with open(file_path, 'w') as file:
            json.dump(data_batch, file, indent=4)
        print(f"Written to {file_path}")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")

# Generate and process permutations in batches
def generate_permutations(ranges, start_index, end_index):
    all_permutations = product(*ranges)
    if end_index is not None:
        all_permutations = islice(all_permutations, start_index, end_index)
    else:
        all_permutations = islice(all_permutations, start_index, None)
    return all_permutations

batch = []
file_index = 1
count = 0
sequence_number = 0

# Keep track of the total number of files created
files_created = 0

permutations = generate_permutations(ranges, start_index, end_index)

for perm in permutations:
    key = ','.join(map(str, perm))
    batch.append({key: sequence_number})
    count += 1
    sequence_number += 1

    # Write to file when batch is full
    if len(batch) == lines_per_file:
        write_to_file(batch, file_index)
        batch = []
        files_created += 1
        
        # Check if the number of files in the current batch is reached
        if files_created >= num_files_in_batch:
            break
        
        file_index += 1

# Write any remaining data
if batch and files_created < num_files_in_batch:
    write_to_file(batch, file_index)

print(f"Total permutations processed: {count}")
print(f"Total files created: {files_created}")

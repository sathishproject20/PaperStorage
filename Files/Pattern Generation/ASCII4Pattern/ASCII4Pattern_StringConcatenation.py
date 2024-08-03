import json
from itertools import product, islice
import os

# Define the number ranges starting from 0 to i - 1 (adjusting for 256 items per range)
i_values = [256, 256, 256, 256]

ranges = [range(0, i) for i in i_values]

# Parameters
lines_per_file = 1000  # Number of lines per file
files_per_batch = 10    # Number of files per batch
output_dir = "output"  # Directory to save files
start_index = 0        # Starting index for permutations
end_index = 10000       # Ending index for permutations (None for no limit)

# Calculate total permutations
total_permutations = 1
for i in i_values:
    total_permutations *= i

# Calculate the number of files required
permutations_count = total_permutations
files_count = (permutations_count // lines_per_file) + (1 if permutations_count % lines_per_file != 0 else 0)

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to write a batch of data to a file
def write_to_file(data_batch, file_index):
    file_path = os.path.join(output_dir, f"data_part_{file_index}.json")
    with open(file_path, 'w') as file:
        json.dump(data_batch, file, indent=4)

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
lines_in_current_file = 0
files_in_current_batch = 0

permutations = generate_permutations(ranges, start_index, end_index)

for perm in permutations:
    key = ''.join(str(x) for x in perm)  # Concatenate the i values as decimal strings without padding
    key_str = str(perm)  # Convert the tuple to a string
    batch.append({key_str: key})
    count += 1
    lines_in_current_file += 1

    # Write to file when batch is full
    if lines_in_current_file == lines_per_file:
        write_to_file(batch, file_index)
        print(f"Batch {files_in_current_batch + 1}, File {file_index}: {lines_per_file} lines written")
        batch = []
        lines_in_current_file = 0
        file_index += 1
        files_in_current_batch += 1
        
        # Start new batch if necessary
        if files_in_current_batch == files_per_batch:
            files_in_current_batch = 0
            print(f"Completed batch {files_in_current_batch + 1}")
            
# Write any remaining data
if batch:
    write_to_file(batch, file_index)
    print(f"Batch {files_in_current_batch + 1}, File {file_index}: {lines_in_current_file} lines written")

print(f"Total permutations processed: {count}")
print(f"Total files created: {file_index - 1}")  # Adjusting for the final file
print(f"Total permutations: {total_permutations}")

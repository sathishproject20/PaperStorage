import json
from itertools import product
import os

def generate_permutations_and_save(start_index, end_index, num_files_in_batch, lines_per_file, output_dir="output"):
    # Define the number ranges
    ranges = [
        range(0, 256),
        range(256, 512),
        range(512, 768),
        range(768, 1024)
    ]
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Function to write a batch of data to a file
    def write_to_file(data_batch, file_index):
        file_path = os.path.join(output_dir, f"data_part_{file_index}.json")
        with open(file_path, 'w') as file:
            json.dump(data_batch, file, indent=4)
    
    # Generate and process permutations in batches
    batch = []
    file_index = 1
    count = 0

    for perm in product(*ranges):
        perm_sum = sum(perm)
        batch.append({"permutation": perm, "sum": perm_sum})
        count += 1
        
        # Write to file when batch is full
        if len(batch) == lines_per_file:
            write_to_file(batch, file_index)
            batch = []
            file_index += 1
            
            # Stop if the required number of files are created
            if file_index > num_files_in_batch:
                break

    # Write any remaining data
    if batch and file_index <= num_files_in_batch:
        write_to_file(batch, file_index)

    print(f"Total permutations processed: {count}")

# Parameters
start_index = 0      # Start index of range
end_index = 10000     # End index of range
num_files_in_batch = 10  # Number of files to create
lines_per_file = 1000   # Number of lines per file

generate_permutations_and_save(start_index, end_index, num_files_in_batch, lines_per_file)

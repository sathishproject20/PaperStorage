import os

def generate_numbers_and_save(start_index, end_index, num_files_in_batch, lines_per_file, output_dir="sequencenumbers"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Function to write a batch of data to a file
    def write_to_file(data_batch, file_index):
        file_path = os.path.join(output_dir, f"SequenceNumbers_{file_index}.txt")
        with open(file_path, 'w') as file:
            for number in data_batch:
                file.write(f"{number}\n")
    
    # Generate numbers and process them in batches
    batch = []
    file_index = 1
    count = 0

    for number in range(start_index, end_index + 1):
        batch.append(number)
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

    print(f"Total numbers processed: {count}")

# Parameters
start_index = 0       # Start index of range
end_index = 65536     # End index of range
num_files_in_batch = 1  # Number of files to create
lines_per_file = 65536    # Number of lines per file

generate_numbers_and_save(start_index, end_index, num_files_in_batch, lines_per_file)

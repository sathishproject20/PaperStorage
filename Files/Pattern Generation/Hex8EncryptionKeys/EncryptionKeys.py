import itertools
import os

def generate_hex_permutations(length=6, start_index=0, end_index=None, max_lines_per_file=65536, max_files_per_directory=1000, base_output_dir='EncryptionKeys'):
    hex_chars = 'ghijklmnopqrstuvwxyz!@#$%^&><_+-*/?=[]{}()~;:'
    total_permutations = len(hex_chars) ** length

    if end_index is None:
        end_index = total_permutations

    # Ensure indices are within the valid range
    start_index = max(0, start_index)
    end_index = min(end_index, total_permutations)

    # Initialize counters
    dir_count = 1
    file_count = 1
    line_count = 0

    # Create the first output directory if it does not exist
    current_output_dir = os.path.join(base_output_dir, f'EncryptionKeys_{dir_count}')
    if not os.path.exists(current_output_dir):
        os.makedirs(current_output_dir)

    # Open the first file
    file_name = os.path.join(current_output_dir, f'EncryptionKeys_{file_count}.txt')
    f = open(file_name, 'w')

    for i, perm in enumerate(itertools.product(hex_chars, repeat=length)):
        if i < start_index:
            continue
        if i >= end_index:
            break
        
        f.write(''.join(perm) + '\n')
        line_count += 1

        if line_count >= max_lines_per_file:
            f.close()
            file_count += 1
            line_count = 0

            if file_count > max_files_per_directory:
                dir_count += 1
                file_count = 1
                current_output_dir = os.path.join(base_output_dir, f'EncryptionKeys_{dir_count}')
                if not os.path.exists(current_output_dir):
                    os.makedirs(current_output_dir)
            
            file_name = os.path.join(current_output_dir, f'EncryptionKeys_{file_count}.txt')
            f = open(file_name, 'w')

    # Close the last file if it was not closed in the loop
    if not f.closed:
        f.close()

    print(f'Files generated in {base_output_dir}, each directory containing up to {max_files_per_directory} files.')

# Example usage
generate_hex_permutations(start_index=0, end_index=65536000, max_lines_per_file=65536)

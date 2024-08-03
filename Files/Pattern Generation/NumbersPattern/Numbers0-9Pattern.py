import itertools

"""
Total Number of Permutations of 0123456789 in 10 Character Length is 3628800

"""

def write_permutations_to_multiple_files(start_index, end_index, lines_per_file, base_filename):
    digits = '0123456789'
    permutations = list(itertools.permutations(digits))
    total_permutations = len(permutations)
    
    if start_index < 0 or end_index > total_permutations or start_index >= end_index:
        raise ValueError("Invalid start or end index.")
    
    current_index = start_index
    file_count = 1
    
    while current_index < end_index:
        filename = f"{base_filename}_part{file_count}.txt"
        with open(filename, 'w') as file:
            for _ in range(lines_per_file):
                if current_index >= end_index:
                    break
                file.write(''.join(permutations[current_index]) + '\n')
                current_index += 1
        file_count += 1

# Usage
start_index = 0
end_index = 3628800  # Adjust this as needed
lines_per_file = 10000  # Adjust this as needed
base_filename = 'permutations'

write_permutations_to_multiple_files(start_index, end_index, lines_per_file, base_filename)

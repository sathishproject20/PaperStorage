import itertools

def generate_ascii_decimal_permutations_within_range(start, end, lines_per_file, base_filename, perm_start_index, perm_end_index):
    # ASCII decimal values from start to end
    ascii_decimals = [str(i) for i in range(start, end + 1)]
    
    # Generate all permutations of length 4
    permutations = itertools.product(ascii_decimals, repeat=4)
    
    # Convert permutations to a list for indexing
    perm_list = list(permutations)[perm_start_index:perm_end_index + 1]
    
    file_index = 1
    line_count = 0
    file = None
    
    try:
        for perm in perm_list:
            if line_count == 0:
                # Close the previous file if it exists
                if file:
                    file.close()
                # Open a new file
                filename = f'{base_filename}_{file_index}.txt'
                file = open(filename, 'w', encoding='utf-8')
                file_index += 1
            
            # Join the tuple to form a string with space-separated values and write it to the file
            file.write(' '.join(perm) + '\n')
            line_count += 1
            
            if line_count >= lines_per_file:
                line_count = 0
        
    finally:
        # Close the last opened file
        if file:
            file.close()

# Example usage: generate permutations from ASCII decimal 0 to 255, 1000 lines per file,
# with permutation indices from 0 to 65536
generate_ascii_decimal_permutations_within_range(0, 255, 65536, 'ascii_decimal_permutations', 0, 65536000)

import itertools

def generate_permutations_to_file(filename):
    # Generate all permutations of '0' and '1' of length 16
    permutations = itertools.product('01', repeat=16)
    
    # Open the file in write mode
    with open(filename, 'w') as file:
        for perm in permutations:
            # Join the tuple to form a string and write it to the file
            file.write(''.join(perm) + '\n')

# Call the function with the desired filename
generate_permutations_to_file('permutations.txt')

import itertools

"""
Total Permutations of 45 Characters in 6 Length String is 8308429287425

"""

def generatePermutationsInRange(startIndex, endIndex, numDigits, fileName):
    assert(numDigits > 0)  # Ensure the number of digits is greater than 0
    characters = 'ghijklmnopqrstuvwxyz!@#$%^&><_+-*/?=[]{}()~;:'  # Define the custom set of characters
    count = 0  # Counter to track the number of permutations written
    with open(fileName, 'w') as fout:  # Open the file in write mode
        for combination in itertools.product(characters, repeat=numDigits):
            if count >= startIndex and count <= endIndex:
                fout.write(''.join(combination) + '\n')  # Write each combination to the file, each on a new line
            count += 1
            if count > endIndex:
                break

if __name__ == "__main__":
    startIndex = 0  # Start index of permutations to generate
    endIndex = 999  # End index of permutations to generate (adjust as needed)
    numDigits = 6  # Number of digits in each permutation
    fileName = "custom_base_values_45Length_range.txt"  # Output file name
    generatePermutationsInRange(startIndex, endIndex, numDigits, fileName)

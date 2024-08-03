import random
import os


"""
Permutations of the Digits 0-9:
When you compute the permutations of the digits 0123456789 you are
considering all possible arrangements of these 10 distinct digits, which is given
by 10! (factorial of 10):
                  10!=10x9x8x7x6x5x4x3x2x1=3,628,800
This number represents the total number of ways to arrange all 10 digits where
each arrangement is unique.
__________________________

Unique 10-Digit Numbers:
When generating unique 10-digit numbers, the range of possible numbers is between
1000000000 and 9999999999 inclusive. This means:
                  Minimum 10-digit number: 1000000000
                  Maximum 10-digit number: 9999999999
                  Total unique 10-digit numbers:
                  9999999999-1000000000+1=9,000,000,000
So, there are 9 billion possible 10-digit numbers.


"""
def generate_unique_numbers(start, end, count):
    """Generate a set of unique numbers within a specified range."""
    if end - start + 1 < count:
        raise ValueError("The range is too small to generate the required number of unique numbers.")
    
    unique_numbers = set()
    while len(unique_numbers) < count:
        number = random.randint(start, end)
        unique_numbers.add(number)
    
    return sorted(unique_numbers)  # Sorting for consistency

def save_numbers_to_files(filename_prefix, numbers, lines_per_file):
    """Save the list of numbers into multiple files with the specified number of lines per file."""
    file_index = 1
    total_numbers = len(numbers)
    for i in range(0, total_numbers, lines_per_file):
        with open(f"{filename_prefix}_{file_index}.txt", "w") as file:
            for number in numbers[i:i + lines_per_file]:
                file.write(f"{number}\n")
        file_index += 1

def main():
    start_index = 0
    end_index = 10000
    num_unique_numbers = end_index - start_index + 1  # Total numbers in range
    lines_per_file = 1000  # Number of lines per file
    filename_prefix = "unique_numbers"

    # Generate unique numbers
    print(f"Generating unique numbers from {start_index} to {end_index}...")
    unique_numbers = generate_unique_numbers(start_index, end_index, num_unique_numbers)
    
    # Save numbers to files
    print("Saving numbers to files...")
    save_numbers_to_files(filename_prefix, unique_numbers, lines_per_file)

    print("Done!")

if __name__ == "__main__":
    main()

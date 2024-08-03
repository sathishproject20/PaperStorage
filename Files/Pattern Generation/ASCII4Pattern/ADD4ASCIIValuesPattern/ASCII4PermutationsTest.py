from itertools import product

# Define the number ranges
ranges = [
        range(0, 256),
        range(256, 512),
        range(512, 768),
        range(768, 1024)
]

# Generate permutations and print the first 10 with their sums
count = 0
for perm in product(*ranges):
    perm_sum = sum(perm)
    print(f"Sequence: {perm}, Sum: {perm_sum}")
    count += 1
    if count == 2000:
        break

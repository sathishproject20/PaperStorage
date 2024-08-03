def encode_two_numbers(a, b, base=1000):
    combined = a * base + b
    return combined

def encode_combined_and_value(combined, value, base=1000):
    final_combined = combined * base + value
    return final_combined

def decode_two_numbers(combined, base=1000):
    a = combined // base
    b = combined % base
    return a, b

def decode_combined_and_value(final_combined, base=1000):
    combined = final_combined // base
    value = final_combined % base
    return combined, value

def encode_four_numbers(a, b, c, d):
    combined1 = encode_two_numbers(a, b)
    combined2 = encode_combined_and_value(combined1, c)
    final_combined = encode_combined_and_value(combined2, d)
    return final_combined

def decode_four_numbers(final_combined):
    combined2, d = decode_combined_and_value(final_combined)
    combined1, c = decode_combined_and_value(combined2)
    a, b = decode_two_numbers(combined1)
    return a, b, c, d

# Original numbers
a = 100
b = 50
c = 25
d = 75

# Encode
final_combined = encode_four_numbers(a, b, c, d)
print(f"Encoded number (final_combined): {final_combined}")

# Decode
decoded_a, decoded_b, decoded_c, decoded_d = decode_four_numbers(final_combined)
print(f"Decoded numbers: a = {decoded_a}, b = {decoded_b}, c = {decoded_c}, d = {decoded_d}")

# Decimal Inputs
A = 3
B = 5

# Number of Bits:
bits = 16

inputs = {"INPUT_Carry": 0}

# binary string, LSB first
a_bits = format(A, f'0{bits}b')[::-1]
b_bits = format(B, f'0{bits}b')[::-1]

for i in range(bits):
    inputs[f"A_bit_{i}"] = int(a_bits[i])
    inputs[f"B_bit_{i}"] = int(b_bits[i])
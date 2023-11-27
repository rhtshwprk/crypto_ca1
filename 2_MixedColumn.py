import copy, random, sys

KEY_LENGTH = 16 

def mix_column(column):
    temp = copy.copy(column) # Store temporary column for operations
    column[0] = galois_mult(temp[0], 2) ^ galois_mult(temp[1], 3) ^ \
                galois_mult(temp[2], 1) ^ galois_mult(temp[3], 1)
    column[1] = galois_mult(temp[0], 1) ^ galois_mult(temp[1], 2) ^ \
                galois_mult(temp[2], 3) ^ galois_mult(temp[3], 1)
    column[2] = galois_mult(temp[0], 1) ^ galois_mult(temp[1], 1) ^ \
                galois_mult(temp[2], 2) ^ galois_mult(temp[3], 3)
    column[3] = galois_mult(temp[0], 3) ^ galois_mult(temp[1], 1) ^ \
                galois_mult(temp[2], 1) ^ galois_mult(temp[3], 2)

def mix_columns(state, nb):
    for i in range(nb):
        # Create column from the corresponding array positions
        column = []
        for j in range(nb): 
            # print(f"state[{j}][{i}]")
            column.append(state[j][i])

        # Mix the extracted column
        mix_column(column)

        # Set the new column in the state
        for j in range(nb): 
            state[j][i] = column[j]

def galois_mult(a, b):
    # Galois field multiplication for AES MixColumns
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1 == 1: p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set == 0x80: a ^= 0x1b
        b >>= 1
    return p % 256

def main():
    # Example state matrix (4x4)
    state = [[0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34]]
    

    nb = 4  # Number of columns in the state matrix

    print("Original State (base 10):")
    for index,i in enumerate(state):
        print (i)

    # Apply mix_columns to the state matrix
    mix_columns(state, nb)

    print("\nState After mix_columns:")
    for row in state:
        print(row)

if __name__ == "__main__":
    main()

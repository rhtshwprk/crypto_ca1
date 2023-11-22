def initial_permutation(plaintext):
    # Initial p-box (64 -> 64)
    initial_permutation_box = [
        58,
        50,
        42,
        34,
        26,
        18,
        10,
        2,
        60,
        52,
        44,
        36,
        28,
        20,
        12,
        4,
        62,
        54,
        46,
        38,
        30,
        22,
        14,
        6,
        64,
        56,
        48,
        40,
        32,
        24,
        16,
        8,
        57,
        49,
        41,
        33,
        25,
        17,
        9,
        1,
        59,
        51,
        43,
        35,
        27,
        19,
        11,
        3,
        61,
        53,
        45,
        37,
        29,
        21,
        13,
        5,
        63,
        55,
        47,
        39,
        31,
        23,
        15,
        7,
    ]

    # Perform the initial permutation
    permuted_text = [plaintext[i - 1] for i in initial_permutation_box]

    return permuted_text


def expansion(right_half):
    # Expansion box (32 to 48 bits)
    expansion_box = [
        32,
        1,
        2,
        3,
        4,
        5,
        4,
        5,
        6,
        7,
        8,
        9,
        8,
        9,
        10,
        11,
        12,
        13,
        12,
        13,
        14,
        15,
        16,
        17,
        16,
        17,
        18,
        19,
        20,
        21,
        20,
        21,
        22,
        23,
        24,
        25,
        24,
        25,
        26,
        27,
        28,
        29,
        28,
        29,
        30,
        31,
        32,
        1,
    ]

    # Perform the expansion
    expanded_text = [right_half[i - 1] for i in expansion_box]

    return expanded_text


def xor(left, right):
    #bitwise XOR between two equal-length lists
    return [l ^ r for l, r in zip(left, right)]


def substitution(expanded_half):
    # S-boxes (48 to 32 bits)
    s_boxes = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        # Using S1 for all boxes
    ]

    # Split the expanded half into 8 chunks of 6 bits
    chunks = [expanded_half[i : i + 6] for i in range(0, len(expanded_half), 6)]

    # Apply S-box substitution to each chunk
    substituted_chunks = []
    for i, chunk in enumerate(chunks):
        row = (chunk[0] << 1) + chunk[5]
        col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
        value = s_boxes[0][row][col]
        substituted_chunks.extend([int(bit) for bit in format(value, "04b")])

    return substituted_chunks


def permutation(substituted_half):
    # Permutation box (32 to 32 bits)
    permutation_box = [
        16,
        7,
        20,
        21,
        29,
        12,
        28,
        17,
        1,
        15,
        23,
        26,
        5,
        18,
        31,
        10,
        2,
        8,
        24,
        14,
        32,
        27,
        3,
        9,
        19,
        13,
        30,
        6,
        22,
        11,
        4,
        25,
    ]

    # Perform the permutation
    permuted_half = [substituted_half[i - 1] for i in permutation_box]

    return permuted_half


def des_round(left_half, right_half, round_key):
    # Expansion
    expanded_half = expansion(right_half)

    # XOR with round key
    xor_result = xor(expanded_half, round_key)

    # Substitution
    substituted_half = substitution(xor_result)

    # Permutation
    permuted_half = permutation(substituted_half)

    # XOR with left half
    new_right_half = xor(left_half, permuted_half)

    return right_half, new_right_half

def array_to_string(arr):
    return "".join(map(str,arr))

def main():
    print("\n")
    print("\t\t\t---Starting DES---")
    print("\t\tROHITASHWA PAREEK: 20CS8048\n\n")

    # Example 64-bit plaintext and 48-bit key
    plaintext = "0010110111110001111101101100100010100110011001001000001100101101"
    key = "001001111100101101010000001001010001110110001100"

    print("Plaintext:\t\t\t\t", plaintext)
    print("Key:\t\t\t\t\t", key,"\n")

    # Convert plaintext and key to lists of bits
    plaintext_bits = [int(bit) for bit in plaintext]
    key_bits = [int(bit) for bit in key]
    # print(plaintext_bits)
    # print(key_bits)


    # Perform initial permutation
    permuted_text = initial_permutation(plaintext_bits)
    print("After initial permutation:\t\t", array_to_string(permuted_text),"\n")

    # Split the permuted text into left and right halves (32 bits each)
    left_half = permuted_text[:32]
    right_half = permuted_text[32:]
    print("Left half:\t\t\t\t", array_to_string(left_half))
    print("Right half:\t\t\t\t", array_to_string(right_half),"\n")


    # Perform one round of DES encryption
    new_left_half, new_right_half = des_round(left_half, right_half, key_bits)
    print("Left half after a round:\t\t", array_to_string(new_left_half))
    print("Right half after a round:\t\t", array_to_string(new_right_half),"\n")

    # Combine the left and right halves after one round
    ciphertext = new_left_half + new_right_half

    # Convert the list back to a string
    ciphertext_str = "".join(map(str, ciphertext))

    print("Ciphertext after one round of DES:\t", ciphertext_str)


if __name__ == "__main__":
    main()

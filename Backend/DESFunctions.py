from tables import ip_table, pc1_table,shift_schedule,pc2_table,e_box_table,s_boxes,p_box_table,ip_inverse_table


def str_to_bin(user_input):
    
        # Convert the string to binary
        binary_representation = ''
        
        for char in user_input:
            # Get ASCII value of the character and convert it to binary
            binary_char = format(ord(char), '08b')
            binary_representation += binary_char
            binary_representation = binary_representation[:64]
        
        # Pad or truncate the binary representation to 64 bits
        binary_representation = binary_representation[:64].ljust(64, '0')
        
        # Print the binary representation
        print("Binary representation of input string: ", binary_representation)
        print(len(binary_representation), 'bits of input string')
        
        return binary_representation
    
    

def binary_to_ascii(binary_str):
    ascii_str = ''.join([chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)])
    return ascii_str




def ip_on_binary_rep(binary_representation):
    
    ip_result = [None] * 64
    
    for i in range(64):
        ip_result[i] = binary_representation[ip_table[i] - 1]

    # Convert the result back to a string for better visualization
    ip_result_str = ''.join(ip_result)
    
    return ip_result_str



def key_in_binary_conv():
    # Original key (can be changed but it should be 8 char)
    original_key = 'abcdefgh'
    binary_representation_key = ''
    
    for char in original_key:
    # Convert the characters to binary and concatenate to form a 64-bit binary string
        binary_key = format(ord(char), '08b') 
        binary_representation_key += binary_key

    
    return binary_representation_key



def generate_round_keys():
    
    # Key into binary
    binary_representation_key = key_in_binary_conv()
    pc1_key_str = ''.join(binary_representation_key[bit - 1] for bit in pc1_table)

    
    # Split the 56-bit key into two 28-bit halves
    c0 = pc1_key_str[:28]
    d0 = pc1_key_str[28:]
    round_keys = []
    for round_num in range(16):
        # Perform left circular shift on C and D
        c0 = c0[shift_schedule[round_num]:] + c0[:shift_schedule[round_num]]
        d0 = d0[shift_schedule[round_num]:] + d0[:shift_schedule[round_num]]
        # Concatenate C and D
        cd_concatenated = c0 + d0

        # Apply the PC2 permutation
        round_key = ''.join(cd_concatenated[bit - 1] for bit in pc2_table)

        # Store the round key
        round_keys.append(round_key)
    return round_keys




def encryption(user_input):
    binary_rep_of_input = str_to_bin(user_input)
    # Initialize lists to store round keys
    round_keys = generate_round_keys()
    print("round_key:" , round_keys)

    ip_result_str = ip_on_binary_rep(binary_rep_of_input)
    print("initial Premution:" , ip_result_str)

    # the initial permutation result is devided into 2 halfs
    lpt = ip_result_str[:32]
    rpt = ip_result_str[32:]
    
    print("left halve:" , lpt)
    print("right halve:" , rpt)



    # Assume 'rpt' is the 32-bit right half, 'lpt' is the 32-bit left half, and 'round_keys' is a list of 16 round keys

    for round_num in range(16):
        print("round no:" , round_num + 1)
        # Perform expansion (32 bits to 48 bits)
        expanded_result = [rpt[i - 1] for i in e_box_table]
        

        # Convert the result back to a string for better visualization
        expanded_result_str = ''.join(expanded_result)
        
        print("expansion:" , expanded_result_str)
        # Round key for the current round
        round_key_str = round_keys[round_num]
        print("Round key for current round:" , expanded_result_str)


        xor_result_str = ''
        for i in range(48):
            xor_result_str += str(int(expanded_result_str[i]) ^ int(round_key_str[i]))
            print(f"{i + 1} Bit:" , expanded_result_str)


        # Split the 48-bit string into 8 groups of 6 bits each
        six_bit_groups = [xor_result_str[i:i+6] for i in range(0, 48, 6)]
        print(f"Split the 48-bit string into 8 groups of 6 bits each:" , six_bit_groups)

        # Initialize the substituted bits string
        s_box_substituted = ''

        # Apply S-box substitution for each 6-bit group
        for i in range(8):
            print(f"apply S-Box {i + 1} -----------------------------------------")
            # Extract the row and column bits
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            col_bits = int(six_bit_groups[i][1:-1], 2)
            print("row bits:" ,  row_bits)
            print("col bits:" , col_bits)

            # Lookup the S-box value
            s_box_value = s_boxes[i][row_bits][col_bits]
            print(f"s-box {i + 1} value:", s_box_value)
            
            # Convert the S-box value to a 4-bit binary string and append to the result
            s_box_substituted += format(s_box_value, '04b')
            print(f"s-box {i + 1} after substituted" , s_box_substituted )

        # Apply a P permutation to the result
        print("Apply Premtuion Box to the result--------------------------------")
        p_box_result = [s_box_substituted[i - 1] for i in p_box_table]
        print("Premtuion Box result:" , p_box_result)

        # # Convert the result back to a string for better visualization
        # p_box_result_str = ''.join(p_box_result)


        # Convert LPT to a list of bits for the XOR operation
        print("Convert left halve to a list of bits for the XOR operation---------------")
        lpt_list = list(lpt)
        print("left halve list:" , lpt_list)
        

        # Perform XOR operation
        print("Perform XOR operation----------------------------------------------------")
        new_rpt = [str(int(lpt_list[i]) ^ int(p_box_result[i])) for i in range(32)]
        print("new Right Halve:" , new_rpt)

        # Convert the result back to a string for better visualization
        new_rpt_str = ''.join(new_rpt)
        print("convert the Right halve to string: ", new_rpt_str)

        # Update LPT and RPT for the next round
        lpt = rpt
        rpt = new_rpt_str
        
        print("update right halve and left havle for next round-----------------------------")
        print("update left halve for next round:", lpt)
        print("update right halve for next round:", rpt)

        # Print or use the RPT for each round

    print('\n')
    # At this point, 'lpt' and 'rpt' contain the final left and right halves after 16 rounds

    # After the final round, reverse the last swap
    final_result = rpt + lpt
    print("After the final round, reverse the last swap:" , final_result)

    # Perform the final permutation (IP-1)
    final_cipher = [final_result[ip_inverse_table[i] - 1] for i in range(64)]
    print(" Perform the final permutation (IP-1)-------------------------------------------")
    print(" IP-1 Result : ", final_cipher)
    

    # Convert the result back to a string for better visualization
    final_cipher_str = ''.join(final_cipher)

    # Print or use the final cipher(binary)
    print("Final Cipher binary:", final_cipher_str, len(final_cipher_str))


    # Convert binary cipher to ascii
    final_cipher_ascii = binary_to_ascii(final_cipher_str)
    print("Final Cipher text:", final_cipher_ascii , len(final_cipher_ascii))
    
    final_plain_text = clean_ascii(final_cipher_ascii)
    print("Final Plain Text:", final_plain_text, len(final_plain_text))


    return final_cipher_str


# decryption of cipher to origional
def clean_ascii(text):
    # Filter out non-printable characters
    return ''.join([char if 32 <= ord(char) <= 126 else '?' for char in text])

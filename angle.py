import cmath
import math

def binary_to_q15_15(binary_string):
    # Determine sign
    if binary_string[0] == '1':
        is_negative = True
    else:
        is_negative = False
    
    # Calculate integer value
    integer_value = int(binary_string, 2)
    
    # If negative, convert to two's complement
    if is_negative:
        integer_value -= 1 << len(binary_string)  # Subtract 2^30
    
    # Convert to Q15.15 format
    decimal_value = integer_value / (1 << 15)
    
    return decimal_value

def binary_to_q13_19(binary_string):
    # Determine sign
    if binary_string[0] == '1':
        is_negative = True
    else:
        is_negative = False
    
    # Calculate integer value
    integer_value = int(binary_string, 2)
    
    # If negative, convert to two's complement
    if is_negative:
        integer_value -= 1 << len(binary_string)  # Subtract 2^30
    
    # Convert to Q15.15 format
    decimal_value = integer_value / (1 << 19)
    
    return decimal_value


def hex_to_binary_real(hex_num, bit_length=None):
    # Remove the '0x' prefix if present
    hex_num = hex_num[2:] if hex_num.startswith("0x") else hex_num

    # Convert the hexadecimal number to an integer
    integer_value = int(hex_num, 16)
    
    # Convert the integer to a binary string and remove the '0b' prefix
    binary_string = bin(integer_value)[2:]
    
    # Pad the binary string to the desired length
    if bit_length:
        binary_string = binary_string.zfill(bit_length)  

    part1 = binary_string[:30]
  #  print(part1)
    
    real_part = binary_to_q15_15(part1)
   # print(real_part)
    return real_part

def hex_to_binary_imag(hex_num, bit_length=None):
    # Remove the '0x' prefix if present
    hex_num = hex_num[2:] if hex_num.startswith("0x") else hex_num

    # Convert the hexadecimal number to an integer
    integer_value = int(hex_num, 16)
    
    # Convert the integer to a binary string and remove the '0b' prefix
    binary_string = bin(integer_value)[2:]

    # Pad the binary string to the desired length
    if bit_length:
        binary_string = binary_string.zfill(bit_length)

   # print(binary_string)    

    part2 = binary_string[30:]
   # print(part2)

    imag_part = binary_to_q15_15(part2)
   # print(imag_part)
    return imag_part

def hex_to_binary_real_toe(hex_num, bit_length=None):
    # Remove the '0x' prefix if present
    hex_num = hex_num[2:] if hex_num.startswith("0x") else hex_num

    # Convert the hexadecimal number to an integer
    integer_value = int(hex_num, 16)
    
    # Convert the integer to a binary string and remove the '0b' prefix
    binary_string = bin(integer_value)[2:]

    #print(binary_string)
    
    # Pad the binary string to the desired length
    if bit_length:
        binary_string = binary_string.zfill(bit_length)  

    part1 = binary_string[32:]
    #print(part1)
    
    real_part = binary_to_q13_19(part1)
    #print(real_part)
    return real_part

def hex_to_binary_imag_toe(hex_num, bit_length=None):
    # Remove the '0x' prefix if present
    hex_num = hex_num[2:] if hex_num.startswith("0x") else hex_num

    # Convert the hexadecimal number to an integer
    integer_value = int(hex_num, 16)
    
    # Convert the integer to a binary string and remove the '0b' prefix
    binary_string = bin(integer_value)[2:]

    # Pad the binary string to the desired length
    if bit_length:
        binary_string = binary_string.zfill(bit_length)

   # print(binary_string)    

    part2 = binary_string[:32]
    #print(part2)

    imag_part = binary_to_q13_19(part2)
    #print(imag_part)
    return imag_part

def calculate_mean_freq_offset(hex_num):

    real_part = hex_to_binary_real(hex_num, bit_length=60)
    imag_part = hex_to_binary_imag(hex_num, bit_length=60)

    #print(real_part)
    #print(imag_part)

    angle_radians = math.atan2(imag_part,real_part)
    #print(angle_radians)

    pi_value = math.pi
    delta2 = (angle_radians * 2048) / ( 2 * pi_value * (2048 + 144))

    mean_freq_off = delta2 * 120
    #print(mean_freq_off)
    return mean_freq_off

def calculate_mean_time_offset(hex_num):

    real_part = hex_to_binary_real_toe(hex_num, bit_length=64)
    imag_part = hex_to_binary_imag_toe(hex_num, bit_length=64)

    #print(f"Real: {real_part:.32f}")
    #print(f"Imag: {imag_part:.32f}")

    angle_radians = math.atan2(imag_part,real_part)
    #print(angle_radians)

    theta = 0.25 * angle_radians

    pi_value = math.pi
    epsilon = (theta * 2048) / ( 2 * pi_value)

    mean_time_off = epsilon

    #print(mean_time_off)

    return mean_time_off

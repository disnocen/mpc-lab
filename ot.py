# this is used for oblivious transfer

import random

# 0. boilerplate
debug = False
# print if debug is true
def debug_print(string):
    """
    print if debug is true
    """
    if debug:
        print(string)

# create a random number
def rand(num):
    """
    create a random number
    :warning: this is not cryptographically secure; use os.urandom instead
    """
    debug_print("rand num base: " + str(num))
    return random.randint(0, num)

# power function mod 
def power(x, y, p):
    """
    :param x: base
    :param y: power
    :param p: modulus
    :return: x^y mod p
    :warning: use this instead of '**' as '**' is slow
    :example: power(2, 3, 5) = 3
    """
    return pow(x, y, p)

# return the inverse of a number mod m
def inv(a, m):
    """
    :param a: number
    :param m: modulus
    :return: inverse of a mod m
    :example: inv(3, 11) = 4
    """
    debug_print("inv of " + str(a))
    return pow(a, m-2, m)

# convert number to 128 bit binary string
def num_to_bin(num):
    """
    :param num: number
    :return: 128 bit binary string
    :example: num_to_bin(3) =
    '0000000000000000000000000000000000000000000000000000000000000011'
    """
    debug_print("num to bin: " + str(num))
    return bin(num)[2:].zfill(128)

# convert string to binary
def string_to_bin(string):
    """
    :param string: string
    :return: binary string
    :example: string_to_bin('abc') = '011000010110001001100011'
    """
    debug_print("string to bin: " + string)

    # encode the string to binary
    binary = ''.join(format(ord(i), '08b') for i in string)

    return binary

    # return ''.join(format(ord(i), 'b') for i in string)

# convert binary to string
def bin_to_string(binary):
    """
    :param binary: binary string
    :return: string
    :example: bin_to_string('011000010110001001100011') = 'abc' see string_to_bin
    """
    debug_print("bin to string: " + binary)
    return ''.join(chr(int(binary[i*8:i*8+8], 2)) for i in range(len(binary)//8))

# return xor of two binary strings
def xor(a, b):
    """
    :param a: binary string
    :param b: binary string
    :return: xor of a and b
    :example: xor('011000010110001001100011', '011000010110001001100011') =
    '000000000000000000000000'
    """
    debug_print("in xor func a is " + str(a))
    debug_print("in xor func b is " + str(b))

    if type(a) == int:
        a = num_to_bin(a)
    if type(b) == int:
        b = num_to_bin(b)
    # if a is a string but not a binary string, convert it to binary
    if type(a) == str and a[0] != '0' and a[0] != '1':
        a = string_to_bin(a)
    if type(b) == str and b[0] != '0' and b[0] != '1':
        b = string_to_bin(b)

    debug_print("xor: " + a + " " + b)

    return ''.join([str(int(a[i]) ^ int(b[i])) for i in range(len(b))])

# 1. create shared parameters
# create a 128 bit prime number
num = 2**128 - 2**97 - 1
gen = 2
C = rand(num-1)


# 2. create keys for bob

def gen_bob_keys(rand_int=C, i =0, mod = num):
    """
    :param rand_int: random integer
    :param i: index
    :param mod: modulus
    :return: bob's keys in two lists
    """ 
    x = rand(mod-2)
    priv_key = [i, x]
    debug_print("bob priv key: " + str(priv_key))
    pub_key = [0,0]
    pow1 = power(gen, x, mod)
    pub_key[i] = pow1
    pub_key[1-i] = (rand_int* inv(pow1,mod)) % mod
    debug_print("bob pub key: " + str(pub_key))
    return priv_key, pub_key

# 3. non interactive oblivious transfer protocol

# 3a. bob sends his public key to alice
def bob_send_pub_key(pub_key):
    return pub_key
# 3b. alice sends the strings to bob
def alice_send_strings(string1, string2, bob_pub_key, mod = num):
    """
    :param string1: string
    :param string2: string
    :param bob_pub_key: bob's public key as created in gen_bob_keys
    :param mod: modulus
    :return: encrypted strings
    """
    y0 = rand(mod-2)
    y1 = rand(mod-2)

    debug_print("alice y0: " + str(y0))
    debug_print("alice y1: " + str(y1))

    alpha0 = power(gen, y0, mod)
    alpha1 = power(gen, y1, mod)

    debug_print("alice alpha0: " + str(alpha0))
    debug_print("alice alpha1: " + str(alpha1))

    beta0 = bob_pub_key[0]
    beta1 = bob_pub_key[1]

    debug_print("alice beta0: " + str(beta0))
    debug_print("alice beta1: " + str(beta1))

    gamma0 = power(beta0, y0, mod)
    gamma1 = power(beta1, y1, mod)

    debug_print("alice gamma0: " + str(gamma0))
    debug_print("alice gamma1: " + str(gamma1))
    alpha = [alpha0, alpha1]
    xored0 = xor(gamma0, string1)
    xored1 = xor(gamma1, string2)
    xored = [xored0, xored1]
    return alpha, xored

# 3b. bob receives the strings from alice and chooses which one to open
def bob_receive_strings(alpha, xored, priv_key, mod = num):
    """
    :param alpha: alpha as created in alice_send_strings
    :param xored: xored as created in alice_send_strings
    :param priv_key: bob's private key as created in gen_bob_keys
    :param mod: modulus
    :return: decrypted string based on the index chosen
    """
    x = priv_key[1]
    i = priv_key[0]
    pow1 = power(alpha[i], x, mod)
    debug_print("bob pow1: " + str(pow1))
    string = xor(pow1, xored[i])
    return string


if __name__ == "__main__":
    bob_i = rand(1)
    bob_priv_key, bob_pub_key = gen_bob_keys(i=bob_i)

    string1 = "hello world"
    string2 = "goodbye world"

    alpha, xored = alice_send_strings(string1, string2, bob_pub_key)
    debug_print("bob alpha0: " + str(alpha[0]))
    debug_print("bob alpha1: " + str(alpha[1]))
    debug_print("bob string1: " + str(xored[0]))
    debug_print("bob string2: " + str(xored[1]))

    string = bob_receive_strings(alpha, xored, bob_priv_key)
    debug_print("bob binary string: " + str(string))
    debug_print("bob string: " + bin_to_string(string))

    if bob_i == 0:
        if (string == string_to_bin(string1)) and (bin_to_string(string) == string1):
            print("bob received string1: " + string1)
        else:
            print("bob did not receive string1")
    else:
        if ( string == string_to_bin(string2) ) and (bin_to_string(string) == string2):
            print("bob received string2: " + string2)
        else:
            print("bob did not receive string2")

    print("possible strings: \'"+string1+"\' and \'"+string2+"\'")
    print("done")


from ot import *

"""
This is a basic example of how to use the OT library to create a 1-of-n OT.
The complexity of this protocol is O(n) and is not secure against malicious Senders and/or Receivers.
The next example will be a secure version of this protocol with a complexity of O(log(n)).
"""


debug = False

def create_pairs_from_strings(strings):
    """
    :param strings: list of strings
    :return: pairs
    :example: create_pairs_from_strings(['a','b','c','d']) = [['a','b'], ['c','d']]
    """
    debug_print("create pairs from strings: " + str(strings), debug=debug)
    pairs = []
    for i in range(0, len(strings), 2):
        pairs.append([strings[i], strings[i+1]])
    return pairs

# this function is used to make sure the i related to Bob choice is 1
def get_i_from_bob_choice(bob_choice):
    if bob_choice % 2 :
        string = (bob_choice-1) //2 # this is the index of the string in the list
    else:
        string = bob_choice //2 # this is the index of the string in the list
    comp = 0
    if bob_choice % 2 :
        comp += 1
    # print the result
    debug_print("Bob's choice is " + str(bob_choice) +" which is at string " + str(string) + " and the component is " + str(comp), debug=debug)
    return string, comp


# make sure the i related to bob choice is comp
def set_i_to_bob_choice(randoms, string, comp):
    randoms[string] = comp
    return randoms

# given a list, gives returns the one from bob choice
def get_string_from_bob_choice(strings, bob_choice):
    string, comp = get_i_from_bob_choice(bob_choice)
    return strings[string]


if __name__ == "__main__":
    # alice has a list of 10000 strings
    alice_strings = [str(i) for i in range(10000)]
    bob_choice = 934 

    m = len(alice_strings)

    if  m%2 == 1:
        alice_strings.append("0000000000000000000000000000000000000000000")
        m += 1

    t = m//2

    alice_pairs = create_pairs_from_strings(alice_strings)

    # for each couple of strings, create a random number
    bob_randoms = [rand(1) for i in range(t)]
    bob_randoms = set_i_to_bob_choice(bob_randoms, *get_i_from_bob_choice(bob_choice))

    # for each couple of strings, create a a pair of keys for Bob
    bob_keys = [gen_bob_keys(i=bob_randoms[i]) for i in range(t)]
    # separate the private keys from the public keys
    bob_private_keys = [bob_keys[i][0] for i in range(t)]
    bob_public_keys = [bob_keys[i][1] for i in range(t)]

    # print them
    debug_print("bob's randoms: " + str(bob_randoms), debug=debug)
    # print a new line
    debug_print("", debug=debug)
    debug_print("Bob's keys: " + str(bob_keys), debug=debug)
    # print a new line
    debug_print("", debug=debug)
    debug_print("Bob's private keys: " + str(bob_private_keys), debug=debug)
    # print a new line
    debug_print("", debug=debug)
    debug_print("Bob's public keys: " + str(bob_public_keys), debug=debug)

    Alpha = []
    Xored = []
    for i in range(t):
        alpha, xored = alice_send_strings(alice_pairs[i][0], alice_pairs[i][1], bob_public_keys[i])
        debug_print("Alice's alpha: " + str(alpha), debug=debug)
        debug_print("Alice's xored: " + str(xored), debug=debug)
        Alpha.append(alpha)
        Xored.append(xored)

    Strings = []
    for i in range(t):
        string_rec = bob_receive_strings(Alpha[i], Xored[i], bob_private_keys[i])
        Strings.append(string_rec)

    bob_string = get_string_from_bob_choice(Strings, bob_choice)
    debug_print("Bob's string: " + bin_to_string(bob_string), debug=debug)
    print("Bob's string: " + bin_to_string(bob_string))
    assert bin_to_string(bob_string) == str(bob_choice)

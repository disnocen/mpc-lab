
# goal: garbled circuit. 2 parties Alice (A) and Bob (B)

# -1. boilerplate
from Crypto.Cipher import AES
from os  import urandom

def to_bytes(x):
    if type(x) == str:
        return x.encode()
    if type(x) == int:
        return x.to_bytes(16,'big')

def print_table(table, var=""):
    print("\nthis is the", var, "table\n")
    for i in table:
        print(i)

def create_aes_key():
    key = urandom(16)
    return key

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return (ciphertext,tag)


def double_encrypt(data,cipher1,cipher2):
    ciphertext, tag = encrypt(data,cipher1)
    ciphertext2, tag2 = encrypt(bytearray(str((ciphertext,tag)), 'utf-8'),cipher2)
    return (ciphertext2,tag2)


if __name__ == "__main__":
    # 0. set the operation
    def operation(x=0,y=0):
        return x*y

    # 1. create the table
    X_card = 5 # X={0...(X_card-1)}
    Y_card = 4 # Y={0...(Y_card-1)}

    table = []
    for i in range(Y_card):
        temp_vec = []
        for j in range(X_card):
            temp_vec.append(operation(i,j))
        table.append(temp_vec)

    print_table(table)


    # 2. encrypt the table
    # 2a. create keys
    key_table = []

    # create the X_card * Y_card keys
    X_keys = [ create_aes_key() for i in range(X_card)]
    Y_keys = [ create_aes_key() for i in range(Y_card)]

    for i in range(Y_card):
        temp_vec = []
        for j in range(X_card):
            temp_vec.append((X_keys[j],Y_keys[i]))
        key_table.append(temp_vec)

    print_table(key_table, "key")

    # 2b. create the encrypted table

    # data = b"ciao"
    # test_enc, tag = encrypt(data, X_keys[0])
    # print(test_enc)
    # print(tag)
    encrypted_table = []
    for i in range(Y_card):
        print("i is", i)
        temp_vec = []
        for j in range(X_card):
            print("  j is", j)
            temp_vec.append(double_encrypt(to_bytes(table[i][j]), X_keys[j], Y_keys[i]))
        encrypted_table.append(temp_vec)

    print_table(encrypted_table,"encrypted")




    # 3. interact 
    # 3a. oblivious transfer
    # 3b. decryption
       # The recipient can obtain the original message using the same key and the incoming triple (nonce, ciphertext, tag):
    # >>> from Crypto.Cipher import AES
    # >>>
    # >>> key = b'Sixteen byte key'
    # >>> cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    # >>> plaintext = cipher.decrypt(ciphertext)
    # >>> try:
    # >>>     cipher.verify(tag)
    # >>>     print("The message is authentic:", plaintext)
    # >>> except ValueError:
    # >>>     print("Key incorrect or message corrupted")



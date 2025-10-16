from Crypto.Cipher import AES
from secrets import token_bytes

# Lengte geven aan de key
key = token_bytes(16)

def encrypt(plaintext):

    # Object waaraan de key en modus wordt meegeven
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    # Getypt bericht wordt meegegeven aan de variabel 'plaintext'
    # plaintext wordt omgezet in bytes en versleuteld met een tag voor extra verificatie
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('ascii'))

    return nonce, ciphertext, tag, key

def decrypt(nonce, ciphertext, tag, key):

    # Object aanroepen waarin de key en modus zit
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # Versleuteld bericht ontsleutelen naar bytes
    plaintext = cipher.decrypt(ciphertext)
    try:
        # Eerst verificatie uitvoeren op de tag, daarna pas de 'plaintext' teruggeven
        cipher.verify(tag)

        # plaintext van bytes weer omzetten naar letters
        return plaintext.decode('ascii')
    except ValueError:
        return False

# Encryptie aanroepen
#nonce, ciphertext, tag, key = encrypt(input("Enter a message: "))
#print(f'Key: {key.hex()}')
#print(f'Ciphertext: {ciphertext}')


# Decryptie aanroepen
#user_key = bytes.fromhex(input("Enter the key in hex format: "))
#plaintext = decrypt(nonce, ciphertext, tag, user_key)

#if not plaintext:
    #print('Key incorrect or message corrupted.')
#else:
    #print(f'Verified message: {plaintext}')
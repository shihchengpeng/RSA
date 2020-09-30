# Inspired from https://medium.com/@ismailakkila/black-hat-python-encrypt-and-decrypt-with-rsa-cryptography-bd6df84d65bc
# Updated to use python3 bytes and pathlib

import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pathlib import Path


def generate_new_key_pair():
    #Generate a public/ private key pair using 4096 bits key length (512 bytes)
    new_key = RSA.generate(4096, e=65537)

    #The private key in PEM format
    private_key = new_key.exportKey("PEM")

    #The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")

    private_key_path = Path('private.pem')
    private_key_path.touch(mode=0o600)
    private_key_path.write_bytes(private_key)

    public_key_path = Path('public.pem')
    public_key_path.touch(mode=0o664)
    public_key_path.write_bytes(public_key)


#Our Encryption Function
def encrypt_plain(plain, public_key):
    #Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)
    plain = zlib.compress(plain)  #壓縮，輸出為bytes
    chunk_max_size = 470    #最大容量
    offset = 0
    end_loop = False
    encrypted = bytearray()

    while not end_loop:
        chunk = plain[offset:offset + chunk_max_size]    #資料

        if len(chunk) % chunk_max_size != 0:        #若等於0，代表資料大小已達最大上限，無需padding
            end_loop = True
            chunk += bytes(chunk_max_size - len(chunk))     #資料後方全部補0

        encrypted += rsa_key.encrypt(chunk)
        offset += chunk_max_size

    return base64.b64encode(encrypted)

#Our Decryption Function
def decrypt_cipher(encrypted_cipher, private_key):

    #Import the Private Key and use for decryption using PKCS1_OAEP
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted_cipher = base64.b64decode(encrypted_cipher)
    chunk_max_size = 512
    offset = 0
    decrypted = bytearray()

    #keep loop going as long as we have chunks to decrypt
    while offset < len(encrypted_cipher):

        chunk = encrypted_cipher[offset: offset + chunk_max_size]
        decrypted += rsakey.decrypt(chunk)
        offset += chunk_max_size

    #return the decompressed decrypted data
    return zlib.decompress(decrypted)


generate_new_key_pair() # run if you don't already have a key pair

private_key = Path('private.pem')
public_key = Path('public.pem')
unencrypted_file = Path('plain.txt')
encrypted_file = unencrypted_file.with_suffix('.dat')

encrypted_msg = encrypt_plain(unencrypted_file.read_bytes(), public_key.read_bytes())
decrypted_msg = decrypt_cipher(encrypted_msg, private_key.read_bytes())

print('destination file : '+str(encrypted_file))
print('\ncipher message :\n'+str(encrypted_msg))
print('\nplain  message :\n'+str(decrypted_msg))
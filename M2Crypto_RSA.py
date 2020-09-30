import M2Crypto
import M2Crypto.BN as BN
def generate_keypair_as_pem(key_len, exponent):
    def empty_callback():
        pass
    rsa = M2Crypto.RSA.gen_key(key_len, exponent, empty_callback)
    # Get RSA Public Key in PEM format
    buf = M2Crypto.BIO.MemoryBuffer('')
    rsa.save_pub_key_bio(buf)
    public_key = buf.getvalue()
    # Get Private Key in PEM format
    buf = M2Crypto.BIO.MemoryBuffer('')
    rsa.save_key_bio(buf, None)
    private_key = buf.getvalue() # RSA Private Key
    return (public_key, private_key)
if __name__ == '__main__':
    keylen = 1024         # 1024 bits
    exponent = 65537  
    padding = M2Crypto.RSA.pkcs1_oaep_padding
    # Generate RSA key-pair in PEM files for public key and private key 
    public_key, private_key = generate_keypair_as_pem(keylen, exponent)
    message = 'This is a plain text data'
    # Use public key to encrypt 'message'
    buf = M2Crypto.BIO.MemoryBuffer('')
    buf.write(public_key)
    rsa1 = M2Crypto.RSA.load_pub_key_bio(buf)
    cipher_message = rsa1.public_encrypt(message, padding)
    # Use private key to decrypt 'cipher_message'
    rsa2 = M2Crypto.RSA.load_key_string(private_key)
    plaintext_message = rsa2.private_decrypt(cipher_message, padding)

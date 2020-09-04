'''import random

def gcd(a, b):
    if a == 0:
        return b
    else:
        gcd(b % a, a)

def ext_gcd(a, b):
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = ext_gcd( b%a ,a)
        return (g, x - (b//a) * y, y)

def gen_key(a,b):
    n = p * q
    fy = (p-1) * (q-1)
    e = 0
    for i in range(2, fy):
        if gcd(i ,fy) == 1:
            e = i
    return n, fy, e

if __name__ == "__main__":
    p = 61
    q = 53
    message = 2014
    n, fy, e = gen_key(p,q)
    r, x, y = ext_gcd(fy,e)
    d = x

    cipher = pow (message, e, n)
    decrypted = pow(cipher, d, n)

    print ("p = " + str(p))
    print ("q = " + str(q))
    print ("n = " + str(n))
    print ("fy = " + str(fy))
    print ("e = " + str(e))
    print ("d = " + str(d))

from fractions import gcd
'''
import random
import sys

def gcd(a, b):
    if a == 0:
        return b
    else:
        return gcd(b % a, a)

def ext_gcd(a, b):
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = ext_gcd( b%a ,a)
        return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = ext_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# 選擇兩個質數以及欲加密的明文(int only)
p = 61
q = 53
n = p * q
message = 3232

# 檢查明文長度
if len(str(n)) < len(str(message)):
	raise Exception('message(' + str(len(str(message))) + \
		') 不能比 n(' + str(len(str(n))) + ') 還要長')

fy = (p - 1) * (q - 1)

while(True):
    e = random.randint(2, fy)
    if gcd(e, fy) == 1:
        break
   
d = modinv( e, fy )

plain = message

#pow(x, y, z) = x * y % z
cipher = pow( plain, e, n ) 

decrypted = pow( cipher, d, n)

# 印出整個過程
print ("--------- Variables ---------")
print ("* p = " + str(p))
print ("* q = " + str(q))
print ("* n = " + str(n))
print ("* fy = " + str(fy))
print ("* e = " + str(e))
print ("* d = " + str(d))
print ("----------- Keys ------------")
print ("* Public (n,e) = (" + str(n) + "," + str(e) + ")")
print ("* Private (n,d) = (" + str(n) + "," + str(d) + ")")
print ("* N Bit = " + str(len(bin(n))))
print ("---------- Messages ---------")
print ("* Plain: " + str(plain))
print ("* Encrypted: " + str(cipher))
if plain == decrypted:
	print ("* Decrypted: " + str(decrypted) + " (Correct)")
else:
	print ("* Decrypted: " + str(decrypted) + " (Failed)")
print ("----------- End -------------")
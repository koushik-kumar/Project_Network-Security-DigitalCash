##-----------------------------------------------------------##
# File:   keygen.py                                           #
# Module: RSA Key generation for digital Cash                 #
# Author: Pragati Sharma                                      #
# Funcionality: This module generates the private and public  #
#         keys of RSA Algorithm for Digital Cash.             #
# Compatibility: Python 3.8.0                                 # 
##-----------------------------------------------------------##

# For RSA implementation importing Crypto Module from Python Package Library. 
import Crypto

# For Encryption Decryption functionality of RSA algorithm importing PKCS1_OAEP from Pypl.
from Crypto.Cipher import PKCS1_OAEP

# This module provides facilities for generating fresh, new RSA keys, constructing them from known components, exporting them, and importing them.
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
f = open('bank_pvt_key.pem','wb')
f.write(key.exportKey('PEM'))
f.close()
f = open('bank_pub_key.pem','wb')
public_key = key.publickey()
f.write(public_key.exportKey('PEM'))
f.close()

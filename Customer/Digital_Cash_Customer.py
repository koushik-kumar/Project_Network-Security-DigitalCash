##-----------------------------------------------------------##
# Module: Customer for digital Cash                           #
# Author: Pragati Sharma                                      #
# Funcionality: This module implements the Bank behavior      #
#         described in Protocol 4 of Digital Cash.            #
# Compatibility: Python 3.8.0                                 # 
##-----------------------------------------------------------##

#####################################
## Begin Imports
# To convert strings/integers to Binary Bit stream. Module imported from Pypl (Python Package Library)
import BitVector
from BitVector import *

# To generate random numbers:
import random

# For RSA implementation importing Crypto Module from Python Package Library. 
import Crypto

# For Encryption Decryption functionality of RSA algorithm importing PKCS1_OAEP from Pypl. It includes SHA1 hash algorithm.
from Crypto.Cipher import PKCS1_OAEP

# This module provides facilities for generating fresh, new RSA keys, constructing them from known components, exporting them, and importing them.
from Crypto.PublicKey import RSA 

# For network connectivity
import socket

# for your code to perform introspection about the system in which its running
import sys  

# To enable encode/decode in base64
import base64

# import only system from os 
import os
from os import system, name 
  
# import sleep to show output for some time period 
from time import sleep 

# Importing Warning to supress DeprecationWarning from getting displayed
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Importing time to add wait delay
import time

## End Imports
#####################################

IP = '127.0.0.1'
bank_addr = (IP, 5005)
merch_addr = (IP, 5006)
BUFFER_SIZE = 1024*64

I_n  = 104  # length of Identity in bits

unused_mo = 0
UMO       = [] 
UMO_S     = []
umo_read  = 0

money_order_no  = 5 
# Number of secret pair per check
secret_pairs_no = 3

#load RSA public key
pub_key = RSA.importKey(open('bank_pub_key.pem').read())

# define our clear function
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


# This module is used to create the listed numbers of money order
# Each money order will have:
# Identity bit strings: identity = id + name (Customer ID and Customer Name).
# The Amount for each money order.
# UniqueID string.
def Create_New_Money_Order(CUSTOMER_ID, CUSTOMER_NAME, no_of_Money_Order, total_amount):
#enforce the length on each item
    CUSTOMER_ID = Force_String_Length(CUSTOMER_ID, 3)
    CUSTOMER_NAME = Force_String_Length(CUSTOMER_NAME, 10)
    AMOUNT = str(total_amount)
    if len(AMOUNT) > 5 :
        print ("Exceeds the allowed transaction limit of $99999 \n")
        return 0
    else :
        AMOUNT = Force_String_Length(AMOUNT,5)
    
    #convert each element into bit strings (Binary format 1's and 0's)
    cust_id_bits   = BitVector(textstring = CUSTOMER_ID)
    cust_name_bits = BitVector(textstring = CUSTOMER_NAME)
    identity = cust_id_bits + cust_name_bits
    
    msg_amt    = BitVector(textstring = AMOUNT)
    msg_uni_id = []
    #Create unique ID to each make unique message strings
    # We are not repeating Amount and Identity or every money order to make it more storage effective
    for i in range(0,no_of_Money_Order):
        UniqueByte = random.getrandbits(100) #returns an random int with 100 bits
        uv = BitVector( intVal = UniqueByte, size = 100)
        msg_uni_id.append(uv)
    return msg_uni_id, msg_amt, identity #returns msg_uni_id as array of BitVector, msg_amt as BitVector and Identity as BitVector

# This is used to force the string length to a fixed new_length.
# If the length is bigger than the number we want it will truncate it by taking the first "new_length" characters.
def Force_String_Length(STRING, new_length):
    length = len(STRING)
    #if length < new_length:
    #     STRING.zfill()
    #if t < n :
    if length < new_length:
        for i in range(0, new_length - length):
            STRING = '0' + STRING
    else:
        STRING = STRING[:new_length]
    return STRING

# To generate Il and Ir strings
# Il is R (random number).
# Ir is S ie (I^R)
def secret_splitting(I):
    Il = []
    Ir = []
    for i in range (0, secret_pairs_no):
       r1  = random.getrandbits(I_n) #returns an random int with I_n bits
       R = BitVector(intVal = r1, size = I_n) # this is R 
       S = I^R # ^ is XOR operation
       Il.append(R)
       Ir.append(S)

    return Il,Ir #returns Il and Ir as arrays of BitVectors
   
# This module encrypts:
# 1 Unique ID (From Create_New_Money_Order)
# 2 Amount (Amount of each money order)
# 3 Identity bit string (Using secret splitting and bit commitment on Identity)
# Using RSA public key (Public key to maintain anonymity of customer)
# We will use SHA1 hash algorithm, RSA PKCS1_OAEP for Encryption and Decryption. base64 encoding decoding is further applied to encrypted code
def RSA_Blind_Signature(msg_id, msg_amt, I):
    #Find the secret splitting pairs for each of the 
    Il,Ir = secret_splitting(I) # we calculated R and S
    
    # Combining all data to form the MO.
    message_I1_bv  = Il[0] + Ir[0]
    message_I1_str = str (message_I1_bv)
    message_I1     = bytearray(message_I1_str, 'utf-8')

    message_I2_bv  = Il[1] + Ir[1]
    message_I2_str = str (message_I2_bv)
    message_I2     = bytearray(message_I2_str, 'utf-8')

    message_I3_bv  = Il[2] + Ir[2]
    message_I3_str = str (message_I3_bv)
    message_I3     = bytearray(message_I3_str, 'utf-8')

    message_ID_bv  = msg_id + msg_amt
    message_ID_str = str (message_ID_bv)
    message_ID     = bytearray(message_ID_str, 'utf-8')

    # Applying RSA blind signature using public key and SHA1 hash function
    cipher = PKCS1_OAEP.new(pub_key)
    # Encrtypting Data
    ciphertext_I1 = cipher.encrypt(message_I1)
    ciphertext_I2 = cipher.encrypt(message_I2)
    ciphertext_I3 = cipher.encrypt(message_I3)
    ciphertext_ID = cipher.encrypt(message_ID)
    # encoding in base64
    ciphertext = base64.encodebytes(ciphertext_I1 + ciphertext_I2 + ciphertext_I3 + ciphertext_ID)

    return ciphertext

# This Module stores the signed MO received from BANK
def Store_Signed_MO(MO_SIGNED):
    with open('SIGNED_MO.txt', 'ab') as fh:
                fh.write(MO_SIGNED)
                fh.close


while 1:
    #clear()
    print("###-------------------------------###")
    print("Welcome to CMPE-209 Credit Union Bank")

    mode = input("To create a new money order, enter '1';\nTo view previously created money orders, press '2';\nTo quit press '3'")
    
    if mode == '1':
        customer_id     = input("Enter the 5- digit Account No: ")
        customer_name   = input("Enter your Name(max 10 chars): ")

        amount = input("Enter the amount to create MO for (less than $99999): ")

        msg_uni_id, msg_amount, Identity = Create_New_Money_Order(customer_id, customer_name, money_order_no, amount)
        m = []
        b = []

        for i in range(0,money_order_no):
            m.append(i)
            m[i] = RSA_Blind_Signature(msg_uni_id[i], msg_amount, Identity)
        Message_req    = "Request_Money_order" #framing request to bank

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Sending the initial request string
        s.sendto(Message_req.encode(),bank_addr)
        # Sending the complete money order data
        for i in range(0,money_order_no):
            s.sendto(m[i],bank_addr)

        #recieve signed MO from bank
        data, addr = s.recvfrom(BUFFER_SIZE)
        Message = data.decode()
        if (Message == "Signing Money order received from customer"):
            MO_SIGNED, addr = s.recvfrom(BUFFER_SIZE)
            print ("*************MO Request Accepted**********************")
            print ("*************Stored Money Order Securely**************")
            Store_Signed_MO(MO_SIGNED)
        elif (Message == "FRAUD"):
            print ("MO Request Rejected")
            print ("*************FRAUD DETECTED**************")
        s.close()
        time.sleep(10) 
        
    elif mode == '2':
        if (os.stat("SIGNED_MO.txt").st_size == 0): 
            print("**********No Money orders to spend***********")
            time.sleep(10) 
        else:
            # Reading 1st unused MO from file
            with open('SIGNED_MO.txt', 'rb') as fh:
                read_MOS=fh.read(1735)
                fh.seek(1735)
                read_rem=fh.read()
                fh.close
            # Removing the read data from file
            with open('SIGNED_MO.txt', 'wb') as fh:
                fh.write(read_rem)
                fh.close
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(read_MOS,merch_addr)
            data, addr = s.recvfrom(BUFFER_SIZE)
            Message = data.decode()
            print (Message)
            time.sleep(10) 
    elif mode == '3':
        exit()
            

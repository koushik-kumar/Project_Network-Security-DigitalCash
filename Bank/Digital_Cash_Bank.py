##-----------------------------------------------------------##
# Module: Customer for digital Cash                           #
# Author: Pragati Sharma                                      #
# Funcionality: This module implements the customer behavior  #
#         described in Protocol 4 of Digital Cash.            #
# Compatibility: Python 3.8.0                                 # 
##-----------------------------------------------------------##

#####################################
## Begin Imports
# To convert strings/integers to Binary Bit stream. Module imported from Pypl (Python Package Library)
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
from os import system, name 
  
# import sleep to show output for some time period 
import time
from time import sleep 

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# To process unique id database
import csv
filename = "bank_database.csv"
## End Imports
#####################################

IP = '127.0.0.1'
bank_addr = (IP,5005)
BUFFER_SIZE = 1024*64
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(bank_addr)
t = 0

amount = []
money_oder_no = 5
for i in range (0,money_oder_no):
    amount.append(i)

#load RSA private key
pvt_key = RSA.importKey(open('bank_pvt_key.pem').read())
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
  
# This module verifies the MO request from customer.
# It verifies the value of n-1 amount.
# If the amount matches, the MO is signed and returned to Customer
# If the amount does not match, Customer is trying to cheat and MO request is rejected
def Process_Money_Order(MO,k,rand2):
    VERIFY = "NULL"
    j = 0
    for i in range (0, k):
        if i in rand2:
            amount[j] = Unblind_RSA_Signature(MO[i])
            j += 1
    j = 0
    for i in range (0, k-2):
        if i in rand2:
            if (amount[j] == amount[j+1]):
                j += 1
                VERIFY = "GOOD"
            else:
                VERIFY = "CHEATER"
    for i in range (0, k):
        if i not in rand2:
            MO_S = MO[i]
            MO_SIGN = Sign_Money_order(amount[i])
    MO_RET = MO_SIGN + MO_S
    return VERIFY, MO_RET

# This is submodule to Process_Money_Order
# It unblinds all the money and only process the amount field.
# No other fields are revealed
def Unblind_RSA_Signature(ciphertext_b64):
    ciphertext    = base64.decodebytes(ciphertext_b64)
    ciphertext_ID = ciphertext[768:1024]

    cipher     = PKCS1_OAEP.new(pvt_key)
    message_ID = cipher.decrypt(ciphertext_ID)
    message_4 = str(message_ID,'utf-8') 
    unique_id = message_4[:100]
    amount    = message_4[100:140]

    amount_int = Amount_to_int (amount)
    return amount_int, 

# This is submodule to Unblind_RSA_Signature.
# It converts the binary amount to integer amount value.
# Each digit of amount is represented by 8 bits.
# Bits 7:4 only have byte encryption detail.
# the value is stored in lower 4 bits
def Amount_to_int (amount): 
    amt_10000 = 0
    amt_1000  = 0
    amt_100   = 0
    amt_10    = 0
    amt_1     = 0
    # For the 10000's place digit
    for i in range (0,4):
        if (amount[i+4] == '1'):
          amt_10000 = amt_10000 + pow(2,3-i)

    # For the 1000's place digit
    for i in range (0,4):
        if (amount[i+12] == '1'):
          amt_1000  = amt_1000  + pow(2,3-i)

    # For the 100's place digit
    for i in range (0,4):
        if (amount[i+20] == '1'):
          amt_100   = amt_100   + pow(2,3-i)

    # For the 10's place digit
    for i in range (0,4):
        if (amount[i+28] == '1'):
          amt_10    = amt_10    + pow(2,3-i)

    # For the 1's place digit
    for i in range (0,4):
        if (amount[i+36] == '1'):
          amt_1     = amt_1     + pow(2,3-i)

    # Multiplying each digit with appropriate multiplying factor to get the integer value of amount
    amount_int = amt_10000 * 10000 + amt_1000 * 1000 + amt_100 * 100 + amt_10 * 10 + amt_1
    return (amount_int)

# This module is submodule to Process_Money_Order
# It signs the Good money order request
def Sign_Money_order(amount):
    message_s_str = "SIGNED" + str (amount)
    message       = bytearray(message_s_str, 'utf-8')
    cipher        = PKCS1_OAEP.new(pvt_key)
    MO_s          = cipher.encrypt(message)
    MO_sign       = base64.encodebytes(MO_s)
    return MO_sign

# This modules verifies the money order given by Merchant for processing
# It verifies banks signature. 
# If signature ok checks unique_id with all unique_ids processed.
# If no fraud is detected credits money and saves money order details
# If fraud is detected checks who commits fraud, Customer or Merchant
# If Customer commits fraud, The identity is revealed
def Verify_Money_Order(MOS, data_d):
    MOS_SIGN = MOS[:349]
    MO       = MOS[349:]
    ciphertext = base64.decodebytes(MOS_SIGN)
    cipher     = PKCS1_OAEP.new(pvt_key)
    message    = cipher.decrypt(ciphertext)
    msg        = str(message,'utf-8') 
    message    = msg[:6]
    amount     = msg[6:]
    if (message == "SIGNED"):
        result = True
    else: 
        result = False

    if (result):
        ciphertext    = base64.decodebytes(MO)
        ciphertext_I1 = ciphertext[:256]
        ciphertext_I2 = ciphertext[256:512]
        ciphertext_I3 = ciphertext[512:768]
        ciphertext_ID = ciphertext[768:1024]

        cipher     = PKCS1_OAEP.new(pvt_key)
        message_I1 = cipher.decrypt(ciphertext_I1)
        message_I2 = cipher.decrypt(ciphertext_I2)
        message_I3 = cipher.decrypt(ciphertext_I3)
        message_ID = cipher.decrypt(ciphertext_ID)

        message_1 = str(message_I1,'utf-8') 
        message_2 = str(message_I2,'utf-8') 
        message_3 = str(message_I3,'utf-8') 
        message_4 = str(message_ID,'utf-8') 
        unique_id = message_4[:100]

        if (data_d[0] == '1'):
            id1 = message_1[:104]
        else:
            id1 = message_1[104:]
        if (data_d[1] == '1'):
            id2 = message_2[:104]
        else:
            id2 = message_2[104:]
        if (data_d[2] == '1'):
            id3 = message_3[:104]
        else:
            id3 = message_3[104:]

        identity = []
        i = 0
        j = 0
        result = True
        rows = []

        with open(filename, 'r') as csvfile: 
        # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            # extracting each data row one by one 
            for row in csvreader: 
                rows.append(row)
                if (rows[i][0] == unique_id):
                    result = False
                    cheater = "Merchant"
                    print ("Duplicate Money Order")
                    if (rows[i][1] != id1):
                        cheater = "Customer"
                        R = rows[i][1]
                        for j in range (0 , 104):
                            if (R[j] != id1[j]):
                                identity.append(1)
                            else:
                                identity.append(0)
                    if (rows[i][2] != id2):
                        cheater = "Customer"
                        R = rows[i][2]
                        for j in range (0 , 104):
                            if (R[j] != id2[j]):
                                identity.append(1)
                            else:
                                identity.append(0)
                    if (rows[i][3] != id3):
                        cheater = "Customer"
                        R = rows[i][1]
                        for j in range (0 , 104):
                            if (R[j] != id3[j]):
                                identity.append(1)
                            else:
                                identity.append(0)
                i += 1
  
        if (result):
            msg = "5 Money Orders credited for the value " + amount
            write_csv = [unique_id, id1, id2, id3]
            with open(filename, 'a') as csvfile: 
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(write_csv)

        else:
            if (cheater == "Merchant"):
                msg = "Merchant Duplicated Money Order. Request Rejected!"
            elif (cheater == "Customer"):
                msg = "Customer with ID" + str(identity) + "Duplicated the Money Order. Request Rejected!"

    print (msg)
    return msg
    
while 1:
    #clear()
    print ("###############################")
    print ("CMPE-209 Credit Union Bank: Internal Server")
    print ("Secured System")
    data, addr = s.recvfrom(BUFFER_SIZE)
    if not data: 
        print("Bank Down, restart")
        break
    message = data.decode()
    MO = []
    if message == "Request_Money_order":
        i = 0
        for i in range (0, money_oder_no):
            MO.append(i)
            MO[i],addr = s.recvfrom(BUFFER_SIZE)
        rand2 = random.sample(range(0,money_oder_no),money_oder_no-1)
        verify, MO_SIGN = Process_Money_Order(MO,money_oder_no,rand2)
        if (verify == "CHEATER"):
            print ("Incorrect Money Order Request")
            msg = "FRAUD"
            s.sendto(msg.encode(),addr)
        else:
            msg = "Signing Money order received from customer"
            print(msg)
            s.sendto(msg.encode(),addr)
            s.sendto(MO_SIGN,addr)
        time.sleep(10)
            
    elif message == "MO_desposit":
        #1. req[1] has the (amt+unique string) + (one of the four pairs)
        #2. decrypt the first message and check for unique string in DB
        #3. if unique string not present already, credit amount, else reply not credited
        print("Received Money Order to Cash out")
        MOS, addr = s.recvfrom(BUFFER_SIZE)
        data, addr = s.recvfrom(BUFFER_SIZE)
        data_d = data.decode()
        msg = Verify_Money_Order(MOS, data_d)
        s.sendto(msg.encode(),addr)
        time.sleep(10)

s.close()    

    

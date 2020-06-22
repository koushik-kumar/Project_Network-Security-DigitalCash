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
S = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
S.bind (merch_addr)

# define our clear function
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# Selects random pairs and sends to the customer
def Select_Secret_Pair ():
    r1  = random.getrandbits(3) #returns an random int with I_n bits
    R = BitVector(intVal = r1, size = 3)
    SP_str = str (R)

    return SP_str


while 1:

    print ("******************************")
    print ("Waiting for Money Order from Customer")
    MOS, addr = S.recvfrom (BUFFER_SIZE)
    cust_addr = addr
    msg_to_bank = "MO_desposit"
    S.sendto (msg_to_bank.encode(), bank_addr)
    print ("Verified Signed Money Order")
    S.sendto (MOS, bank_addr)
    msg = Select_Secret_Pair ()
    print ("Sending partial pairs")
    S.sendto (msg.encode(), bank_addr) #send the partial pairs or Error message to customer
    print ("Depositing Money Order to Bank")
    data, addr = S.recvfrom (BUFFER_SIZE)
    Message = data.decode()
    print (Message)
    if (Message[0] == '5'):
        msg = "Payment Received"
    else:
        msg = "Payment Rejected by Bank"
    S.sendto(msg.encode(),cust_addr)
    time.sleep(10)

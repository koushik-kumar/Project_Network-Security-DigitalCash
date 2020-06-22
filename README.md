# Project Setup

## Current project is designed using python 3.8.0
There may be a need to install a few python packages from pypl (python package library).
a. BitVector
b. pycryptodome==3.4.3

### If there is an error for missing package library, please install using:
pip3 install <package_name>

### Step 1:
Open Three Terminals or three tabs in a terminal.

### Step 2:
i. In terminal one load Bank function
ii. In terminal two load Customer function
iii. In terminal three load Merchant function

### Step 3:
Follow steps in the terminal for Customer Function. (No user inputs are needed for Bank and Merchant Functions)

On generating a new money order, the signed money order details are stored in file SIGNED_MO.txt in Customer directory.
On Successfully debiting a Money Order the details of money order (unique_id and identity informations) are stored in bank_database.csv in Bank Directory.

To create a cheating scenario, this file can be edited to duplicate MO information or to corrupt money order.
If any-errors are seen during the usage of signed money order, please clean all data in SIGNED_MO.txt and execute all three programs again.

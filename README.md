# Project Setup

Python version  - 3.8.0

#### For other packages - pip3 install <package_name>

* BitVector
* pycryptodome==3.4.3




### Step 1:
Open three terminals or terminal tabs

### Step 2:
1. In first terminal, run Bank function
2. In second terminal, run Customer function
3. In the third, run Merchant function

### Step 3:
Follow steps in the terminal for Customer Function. (No user inputs are needed for Bank and Merchant Functions)

On generating a new money order, the signed money order details are stored in file SIGNED_MO.txt in Customer directory.
On Successfully debiting a Money Order the details of money order (unique_id and identity informations) are stored in bank_database.csv in Bank Directory.

To create a cheating scenario, this file can be edited to duplicate MO information or to corrupt money order.
If any-errors are seen during the usage of signed money order, please clean all data in SIGNED_MO.txt and execute all three programs again.

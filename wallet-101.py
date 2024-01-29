# ABOUT
# This is a simple wallet based on the python library bitcoinlib

# INSTALLATION
# Run this command to install the bitcoinlib library:
#	`pip install bitcoinlib`

# Run the command below to install the necessary dependencies on Ubuntu
# `apt install build-essential python3-dev libgmp3-dev pkg-config postgresql postgresql-contrib mariadb-server libpq-dev libmysqlclient-dev pkg-config`

# BITCOIN NODE SETUP
# The wallet works on the testnet chain.
# Please make sure you have server and txindex option set to 1

# If the above is met, you are ready to interact with this wallet

## Create a wallet
## To create a wallet run this command:
## `python3 wallet-101.py --createwallet wallet_name`

## Get an address
## After creatin a wallet you get a single address by default. You can generate more by running this command:
## `python3 wallet-101.py --getaddress wallet_name`

## Sweep Satoshis
## To send satoshis in all your wallets, run he command:
## `python3 wallet-101.py --send wallet_name`
## This will send back all the bitcoin to a testnet faucet address that is hardcoded

import sys
import argparse
from bitcoinlib.wallets import *
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey
from bitcoinlib.keys import Key
from bitcoinlib.wallets import wallet_create_or_open

def normalKey():
	print("Create a new key with a public and private key architecture")
	k = Key()
	k.info()

def HdKey():
	print("Cretae a hierachical deteministic key")
	k = HDKey(witness_type='segwit')
	k.info()

def MnemonicKey():
	print('generate a HD key from a mnemonic phrase')
	phrase = Mnemonic().generate()
	print(phrase)
	k = HDKey.from_passphrase(phrase)
	print(k.private_hex)

def createOpenWallet(name):
	# The wallet class is used to store and manage keys, check for new utxo's, create, sign and send transactions.
	w = wallet_create_or_open(name, network='testnet', witness_type='segwit')
	w.info()
 
def getAddress(name):
	w = Wallet(name)
	wk = w.new_key()
	print("Your new address is " % wk.address)
 
def sendTransaction(name):
    w = Wallet(name)
    # Sweep all UTXOs and send them back to the testnet faucet address
    t = w.sweep('tb1q5tsjcyz7xmet07yxtumakt739y53hcttmntajq')
    t.info()
 

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process command-line arguments.')

    # Add arguments
    parser.add_argument('--createwallet', help='Specify the action to perform')
    parser.add_argument('--getaddress', help='Specify the action to perform')
    parser.add_argument('--send', help='Specify the action to perform')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Check the value of the 'todo' argument and call the corresponding function
    if args.createwallet:
        createOpenWallet(args.createwallet)
    elif args.getaddress:
        getAddress(args.getaddress)
    elif args.send:
        sendTransaction(args.send)
    else:
        print("Invalid or missing argument. Use --todo arg")

if __name__ == "__main__":
    main()


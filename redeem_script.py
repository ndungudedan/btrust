import hashlib
import base58
import argparse
from bitcoinlib.transactions import *
from bitcoinlib.encoding import *
from bitcoinlib.transactions import Transaction, Output, Input
from bitcoinlib import *
from bitcoinlib.services.services import *
from bitcoinlib.wallets import *

def generateRedeemScript(preimage_hex):
    preimage_bytes = to_bytes(preimage_hex)
    lock_hash = hashlib.sha256(preimage_bytes).digest()
    redeem_script = bytes([0xa8]) + lock_hash + bytes([0x87])
    bth= to_hexstring(redeem_script)
    print(bth)
    
def deriveAddress(redeem_script_hex):
    redeem_script_bytes = to_bytes(redeem_script_hex)
    hash160_bytes = hash160(redeem_script_bytes)
    address_bytes = b'\x05' + hash160_bytes
    address = base58.b58encode_check(address_bytes).decode('utf-8')
    print(address)

def sendCoinsToAddress(wallet_name):
    # Use a previously funded wallet to send funds from
    w = Wallet(wallet_name)
    # Sweep all UTXOs and send them to the address
    t = w.sweep('3BLEeBm37w4aHL5Bq23rZQqjFjrWZGZ73p')
    t.info()

def main():
    parser = argparse.ArgumentParser(description='Process command-line arguments.')
    parser.add_argument('--redeemscript', help='Specify the action to perform')
    parser.add_argument('--deriveaddress', help='Specify the action to perform')
    parser.add_argument('--sendcoins', help='Specify the action to perform')
    args = parser.parse_args()

    if args.redeemscript:
        generateRedeemScript(args.redeemscript)
    elif args.deriveaddress:
        deriveAddress(args.deriveaddress)
    elif args.sendcoins:
        sendCoinsToAddress(args.sendcoins)
    else:
        print("Invalid or missing argument. Use --todo arg")
    
if __name__ == "__main__":
    main()
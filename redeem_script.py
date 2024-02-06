import hashlib
import base58
import argparse
from bitcoinlib.transactions import *
from bitcoinlib.encoding import *
from bitcoinlib.transactions import *
from bitcoinlib import *
from bitcoinlib.services.services import *
from bitcoinlib.services.services import Service
from bitcoinlib.wallets import *

# Run the command:
# python3 redeem_script.py --redeemscript 427472757374204275696c64657273  
def generateRedeemScript(preimage_hex):
    preimage_bytes = to_bytes(preimage_hex)
    lock_hash = hashlib.sha256(preimage_bytes).digest()
    redeem_script = bytes([0xa8]) + lock_hash + bytes([0x87])
    print("Bytes: ",redeem_script)
    bth= to_hexstring(redeem_script)
    print("Hex code: ",bth)

# Run the command:
# python3 redeem_script.py --deriveaddress <redeem script hex code>    
def deriveAddress(redeem_script_hex):
    redeem_script_bytes = to_bytes(redeem_script_hex)
    hash160_bytes = hash160(redeem_script_bytes)
    # using the prefix xc4 to indicate the testnet network
    # use x05 to indicate mainnet
    address_bytes = b'\xc4' + hash160_bytes
    address = base58.b58encode_check(address_bytes).decode('utf-8')
    print(address)

# Run the command:
# python3 redeem_script.py --sendcoins <wallet name> --address <address>
# Address is: 2N2tShvh4jPZvV7hjW9fjBMpzU64gJvfvZf
def sendCoinsToAddress(wallet_name,address):
    # Use a previously funded wallet to send funds from
    w = Wallet(wallet_name)
    # Sweep all UTXOs and send them to the address
    t = w.sweep(address,fee=1000)
    t.info()
    print("Tx Verification Status: ",t.verify())
    res = Service(network="testnet").sendrawtransaction(t.raw_hex())
    print(res)

# Run the command:
# python3 redeem_script.py --spend <utxo transaction hash>
def spendCoins(prev_txid):
    amount=100
    tx = Transaction(network="testnet",fee_per_kb=10)
    tx.add_input(prev_txid=prev_txid,
                 script_type="p2sh_multisig",
                 sigs_required=1,
                 public_hash=bytes.fromhex("a816e05614526c1ebd3a170a430a1906a6484fdd203ab7ce6690a54938f5c44d7d87"),
                 keys=bytes.fromhex("a816e05614526c1ebd3a170a430a1906a6484fdd203ab7ce6690a54938f5c44d7d87"),
                 output_n=0,strict=False)
    
    # Both addresses to receive the coins belong to testnet faucets
    tx.add_output(address="mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB", value=amount)
    tx.add_output(address="tb1q5tsjcyz7xmet07yxtumakt739y53hcttmntajq", value=tx.change)
    tx.sign()
    tx.info()
    print("Tx Verification Status: ",tx.verify())
    res = Service(network="testnet").sendrawtransaction(tx.raw_hex())
    print(res)
    

def main():
    parser = argparse.ArgumentParser(description='Process command-line arguments.')
    parser.add_argument('--redeemscript', help='Specify the action to perform')
    parser.add_argument('--deriveaddress', help='Specify the action to perform')
    parser.add_argument('--sendcoins', help='Specify the action to perform')
    parser.add_argument('--spend', help='Specify the action to perform')
    parser.add_argument('--address', help='Specify the action to perform')
    parser.add_argument('--script', help='Specify the action to perform')
    args = parser.parse_args()

    if args.redeemscript:
        generateRedeemScript(args.redeemscript)
    elif args.deriveaddress:
        deriveAddress(args.deriveaddress)
    elif args.sendcoins:
        sendCoinsToAddress(args.sendcoins,args.address)
    elif args.spend:
        spendCoins(args.spend)
    else:
        print("Invalid or missing argument. Use --todo arg")
    
if __name__ == "__main__":
    main()

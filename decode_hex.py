# How to execute commands for this file:
# Run the command below on your terminal
# `python3 decode_hex.py --decodehex <raw_hex>`

# For example:

# python3 decode_hex.py --decodehex 020000000001010ccc140e766b5dbc884ea2d780c5e91e4eb77597ae64288a42575228b79e234900000000000000000002bd37060000000000225120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9cae81c00000000000016001416d31d7632aa17b3b316b813c0a3177f5b6150200140838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e


import argparse
from bitcoinlib.transactions import *

def decode_transaction(hex_string):
    # trans=transaction_deserialize(hex_string,'testnet',False)
    trans=Transaction.parse_hex(hex_string,False,'bitcoin')
    print(trans)
    print("Version:", trans.version)
    print("Locktime:", trans.locktime)
    print("Inputs:", trans.inputs)
    print("Outputs:", trans.outputs)

# Test case
hex_string = "020000000001010ccc140e766b5dbc884ea2d780c5e91e4eb77597ae64288a42575228b79e234900000000000000000002bd37060000000000225120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9cae81c00000000000016001416d31d7632aa17b3b316b813c0a3177f5b6150200140838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e"


def main():
    parser = argparse.ArgumentParser(description='Process command-line arguments.')
    parser.add_argument('--decodehex', help='Specify the action to perform')
    args = parser.parse_args()
    decode_transaction(args.decodehex)
if __name__ == "__main__":
    main()
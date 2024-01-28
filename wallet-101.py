
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

def createOpenWallet():
	# The wallet class is used to store and manage keys, check for new utxo's, create, sign and send transactions.
	w = wallet_create_or_open('bitcoinlib-testnet1', network='testnet', witness_type='segwit')
	wk = w.new_key()
	print("Deposit to address %s to get started" % wk.address)
	n_utxos = w.utxos_update()
	if n_utxos:
		print("Found new unspent outputs (UTXO's), we are ready to create a transaction")
	w.info()
 
def sendTransaction():
    w = wallet_create_or_open('bitcoinlib-testnet1', network='testnet', witness_type='segwit')
    w.info()
    # Sweep all UTXOs and send them back to the testnet faucet address
    t = w.sweep('tb1q5tsjcyz7xmet07yxtumakt739y53hcttmntajq')
    t.info()
 
sendTransaction()


import csv

# We declare a class object 
class Transaction:
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = parents.split(';') if parents else []
        self.children = []
        self.included = False

# We sort the fee from highest to lowest.
# This is utilized by the in built sort function
    def __lt__(self, other):
        return self.fee > other.fee

def parse_mempool_csv(file_path):
    # Defining a dictionary to hold the mempool transactions: The key is the txid and value is the Transaction object 
    # 'tx_id': Transaction()
    transactions = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            txid, fee, weight, parents = row[0].split(',')
            transactions[txid] = Transaction(txid, fee, weight, parents)
            
    # Finding the parents and assigning them their chilren txids
    for txid, tx in transactions.items():
        for parent_txid in tx.parents:
            transactions[parent_txid].children.append(tx)
    return transactions

def construct_block(transactions, max_weight):
    block = []
    current_weight = 0

    def add_transaction_to_block(tx):
        nonlocal current_weight
        current_weight += tx.weight
        tx.included = True
        block.append(tx)

    def explore(transaction):
        if transaction.included:
            return
        for parent_txid in transaction.parents:
            explore(transactions[parent_txid])
        add_transaction_to_block(transaction)

# Sort the transactions
    for tx in sorted(transactions.values()):
        if not tx.included:
            explore(tx)
            if current_weight > max_weight:
                break

    return block

def write_block_to_file(block, file_path):
    with open(file_path, 'w') as f:
        for tx in block:
            f.write(tx.txid + '\n')

if __name__ == "__main__":
    mempool_file_path = 'mempool.csv'
    max_block_weight = 4000000
    
    transactions = parse_mempool_csv(mempool_file_path)
    block = construct_block(transactions, max_block_weight)
    write_block_to_file(block, 'block.txt')

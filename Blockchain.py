import hashlib
import time
import json
import copy

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = str(self.index) + self.previous_hash + json.dumps(self.transactions) + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", [], int(time.time()))

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_reward_address):
        block = Block(len(self.chain), self.get_last_block().hash, self.pending_transactions, int(time.time()))
        block = self.proof_of_work(block)
        self.chain.append(block)
        self.pending_transactions = [self.create_transaction(None, miner_reward_address, 10)]  

    def create_transaction(self, sender, recipient, amount):
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        return transaction

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append(self.create_transaction(sender, recipient, amount))

    def proof_of_work(self, block, difficulty=4):
        while block.hash[:difficulty] != '0' * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

blockchain = Blockchain()

while True:
    print("\nBlockchain Menu:")
    print("1. Add Transaction")
    print("2. Mine Block")
    print("3. Display Blockchain")
    print("4. Validate Blockchain")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        sender = input("Enter sender: ")
        recipient = input("Enter recipient: ")
        amount = float(input("Enter amount: "))
        blockchain.add_transaction(sender, recipient, amount)
        print("Transaction added to pending transactions.")

    elif choice == '2':
        miner_reward_address = input("Enter miner's reward address: ")
        blockchain.mine_pending_transactions(miner_reward_address)
        print("Block mined successfully.")

    elif choice == '3':
        for block in blockchain.chain:
            print("Block #", block.index)
            print("Hash:", block.hash)
            print("Previous Hash:", block.previous_hash)
            print("Transactions:", block.transactions)
            print("Timestamp:", block.timestamp)
            print("Nonce:", block.nonce)
            print("----------")

    elif choice == '4':
        is_valid = blockchain.is_chain_valid()
        if is_valid:
            print("Blockchain is valid.")
        else:
            print("Blockchain is not valid.")

    elif choice == '5':
        print("Exiting the program.")
        break

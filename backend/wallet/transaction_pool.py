from backend.wallet.transaction import Transaction


class TransactionPool:
    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        """
        Set a transactun in the transaction pool.
        """
        self.transaction_map[transaction.id] = transaction

    def existing_transaction(self, address):
        """
        Find a transaction generated bu the address in the transaction pool
        """
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction
            else:
                return None

    def transaction_data(self):
        """
        Return the transactions of the transaction pool represented 
        in their json serialized form
        """
        return list(map(
                lambda transaction: Transaction.to_json(
                    transaction), self.transaction_map.values())
        )

    def clear_blockchain_transactions(self, blockchain):
        """
        Delete blockchain recorded transactions from the transaction pool.
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass
import time

from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce',
    'block_time': 'genesis_time'
}


class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryprocurrency.
    """

    def __init__(self,  timestamp, last_hash, hash, data, difficulty, nonce, block_time):
        self.data = data
        self.timestamp = timestamp
        self.hash = hash
        self.last_hash = last_hash
        self.difficulty = difficulty
        self.nonce = nonce
        self.block_time = block_time

    def __repr__(self) -> str:
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    #Allows equality override to compare classes of this type
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes/

        """
        return self.__dict__
    
    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until a block hash is
        found that meets the leading 0's proof of work requirement. 
        """


        difficulty = last_block.difficulty
  

        timestamp = time.time_ns()
        last_hash = last_block.hash
        #difficulty = last_block.difficulty

        #difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, last_hash, data,  nonce)

        block_time = timestamp - last_block.timestamp
        difficulty = Block.adjust_difficulty(last_block, block_time)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce, block_time)

    @staticmethod
    def genesis():
        """
        Generate the genesis block
        """
        # return Block(
        #              timestamp=GENESIS_DATA['timestamp'],
        #              last_hash=GENESIS_DATA['last_hash'],
        #              hash=GENESIS_DATA['hash'],
        #              data=GENESIS_DATA['data']
        #              )
        return Block(**GENESIS_DATA)
        
    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation back in to a block instance
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, block_time):
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for quickly mined blocks.
        Decreade the difficulty for slowly mined blocks.
        """
    
        if (block_time) < MINE_RATE:
            return last_block.difficulty + 1

        elif (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate lock by enforcing the following rules:
        -- the block must have the proper last_hash reference
        -- the block must meet the proof of work requirement
        -- the difficulty must only adjust by 1
        -- the block hash must be a valid combination of the block fields
        """

        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')

        if hex_to_binary(block.hash)[0:last_block.difficulty] != '0' * last_block.difficulty:
            #print(hex_to_binary(block.hash)[0:block.difficulty])
            raise Exception('The proof of work requirement was not met')

        if abs(block.difficulty - last_block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by one')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')


def main():
    genesis_block = Block.genesis()

    good_block = Block.mine_block(genesis_block, 'foo')

    try:
        Block.is_valid_block(genesis_block, good_block)
    except Exception as e:
        print(f'is_valid_block: {e}')


if __name__ == '__main__':
    main()

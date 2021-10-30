from backend.blockchain import blockchain
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

import pytest


def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(
            [Transaction.to_json(Transaction(Wallet(), 'recipient', i))]
        )
    return blockchain


def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_is_valid_chain_bad_genesis(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'evil_hash'

    with pytest.raises(Exception, match='The genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_replace_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)

    assert blockchain.chain == blockchain_three_blocks.chain


def test_replace_chain_not_longer(blockchain_three_blocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match='Cannot replace.  The incoming chain must be longer.'):
        blockchain_three_blocks.replace_chain(blockchain.chain)


def test_replace_chain_bad_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'evil_hash'

    with pytest.raises(Exception, match='Cannot replace. The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_three_blocks.chain)


def test_valid_transacction_chain(blockchain_three_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def is_valid_transaction_chain_duplicate_transactions(blockchain_three_blocks):
    transaction = Transaction.to_json(Transaction(Wallet(), 'recipient', 1))

    blockchain_three_blocks.add_block([transaction, transaction])

    with pytest.raises(Exception, match='is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_multiple_rewards(blockchain_three_blocks):
    reward_1 = Transaction.to_json(Transaction.reward_transaction(Wallet()))
    reward_2 = Transaction.to_json(Transaction.reward_transaction(Wallet()))

    blockchain_three_blocks.add_block([reward_2, reward_1])

    with pytest.raises(Exception, match='one mining reward per block'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_bad_transacction(blockchain_three_blocks):
    bad_transaction = Transaction(Wallet(), 'recipient', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_three_blocks.add_block([Transaction.to_json(bad_transaction)])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

    def test_is_valid_transaction_chain_bad_historic_balance(blockchain_three_blocks):
        wallet = Wallet()
        bad_transaction = Transaction(wallet, 'recipient', 1)
        bad_transaction.output[wallet.address] = 9000
        bad_transaction.input['amount'] = 9001
        bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

        blockchain_three_blocks.add_block([Transaction.to_json(bad_transaction)])

        with pytest.raises(Exception, match='has an invalid input amount'):
            Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

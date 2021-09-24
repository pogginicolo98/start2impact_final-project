import password

from web3 import Web3


def write_message_on_chain(message):
    """
     Create a new Ethereum transaction and send it on chain.

     * EIP 1559-style transaction
    """

    w3 = Web3(Web3.HTTPProvider(password.network_url))
    address = password.address
    private_key = password.private_key

    basic_tx = {
        'from': address,
        'to': '0x0000000000000000000000000000000000000000',
        'amount': w3.toWei(0, 'ether'),
        'data': message.encode('utf-8')
    }
    estimated_gas = w3.eth.estimate_gas(basic_tx)
    max_priority_fee = w3.eth.max_priority_fee
    max_fee = estimated_gas + max_priority_fee
    nonce = w3.eth.get_transaction_count(address)
    chain_id = w3.eth.chain_id

    signed_tx = w3.eth.account.sign_transaction(dict(
        to=basic_tx['to'],
        value=basic_tx['amount'],
        data=basic_tx['data'],
        gas=estimated_gas,
        maxPriorityFeePerGas=max_priority_fee,
        maxFeePerGas=max_fee,
        nonce=nonce,
        chainId=chain_id,
        type=2,
    ), private_key)
    tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_id = w3.toHex(tx)
    return tx_id

import password

from web3 import Web3


def write_message_on_chain(message):
    """
     Create a new Ethereum transaction and send it on chain.
    """

    w3 = Web3(Web3.HTTPProvider(password.network_url))
    address = password.address
    private_key = password.private_key
    nonce = w3.eth.get_transaction_count(address)
    destination = '0x0000000000000000000000000000000000000000'
    data = message.encode('utf-8')
    gas_price = w3.eth.gas_price
    value = w3.toWei(0, 'ether')
    estimated_gas = w3.eth.estimate_gas({'from': address, 'to': destination, 'amount': value, 'data': data})
    signed_tx = w3.eth.account.sign_transaction(dict(
        nonce=nonce,
        gasPrice=gas_price,
        gas=estimated_gas,
        to=destination,
        value=value,
        data=data
    ), private_key)
    tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_id = w3.toHex(tx)
    return tx_id

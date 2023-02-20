from solcx import compile_standard, install_solc

# install_solc('0.6.0')
import json
from web3 import Web3


# Read the contents of the SimpleStorage.sol contract file
with open("zavrsni.sol", "r") as file:
    sol_file = file.read()

# Compile the Solidity contract using the solcx package
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"zavrsni.sol": {"content": sol_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Extract the bytecode and ABI from the compiled contract
# bytecode
bytecode = compiled_sol["contracts"]["zavrsni.sol"]["Zavrsni"]["evm"][
    "bytecode"
]["object"]

# abi
abi = compiled_sol["contracts"]["zavrsni.sol"]["Zavrsni"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337

my_address = "0x0062CC1915133d2d75E9f14f7Ad951c69b86A956"
private_key = "0x1b5ecd8c3f05eacd35ba3b231d6f1cf4d343649d1f85d549c91e75095391bc51"

Zavrsni = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)

name = "VrsaToken"
totalSupply = 1000

transaction = Zavrsni.constructor(name, totalSupply).build_transaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt['contractAddress']
Zavrsni_2 = w3.eth.contract(address = contract_address, abi=abi)





burn = 30
mint = 10
amount_of_sent_tokens = 100
second_address ="0x11bA2861CD018909d7C697E4F794b5B495406f16"


print("Initial total supply:", Zavrsni_2.functions.totalSupply().call())
balance_our = Zavrsni_2.functions.checkBalanceOf(my_address).call()
print("Stanje našeg računa(owner):", balance_our)
balance_second_account = Zavrsni_2.functions.checkBalanceOf(second_address).call()
print("Stanje drugog računa:", balance_second_account)





Zavrsni_2.functions.mint(mint).transact({'from': my_address})

print("Minting ", mint, "tokens")
print("Total supply after mint:", Zavrsni_2.functions.totalSupply().call())


# Burnanje tokena
Zavrsni_2.functions.burn(burn).transact({'from': my_address})

print("Burning ", burn, "tokens")
print("Total supply after burn:", Zavrsni_2.functions.totalSupply().call())





print("Transfering from one address to another ")
balance_our = Zavrsni_2.functions.checkBalanceOf(my_address).call()
print("Balance of our account:", balance_our)
balance_second_account = Zavrsni_2.functions.checkBalanceOf(second_address).call()
print("Balance of second account", balance_second_account)


Zavrsni_2.functions.transfer(second_address,amount_of_sent_tokens).transact({'from': my_address})

balance_our = Zavrsni_2.functions.checkBalanceOf(my_address).call()
print("New state of our account:", balance_our)
balance_second_account = Zavrsni_2.functions.checkBalanceOf(second_address).call()
print("New state of second account:", balance_second_account)



balance = w3.eth.getBalance(my_address)
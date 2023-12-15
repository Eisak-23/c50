from eth_account import Account
from mnemonic import Mnemonic
from web3 import Web3

# Infura endpoint para Ethereum Rinkeby (obtén tu propia clave API en https://infura.io/)
infura_url = "https://sepolia.infura.io/v3/6cfa3e90aa544d3cad27fecc8926ecf0"

# Crear una instancia de Web3
w3 = Web3(Web3.HTTPProvider(infura_url))
Account.enable_unaudited_hdwallet_features()
# Generar una frase semilla aleatoria
mnemo = Mnemonic("english")
mnemonic = mnemo.generate(128)  # 128 es la longitud en bits, ajusta según sea necesario

# Derivar la cuenta desde la frase semilla
account = Account.from_mnemonic(mnemonic)

# Imprimir la dirección generada desde la frase semilla
print(f"Dirección: {account.address}")

# Imprimir la llave privada (solo para fines educativos, no lo hagas en producción)
print(f"Llave privada: {account._private_key.hex()}")

# llave
print(f"Frase mneomic {mnemonic}")

# Puedes utilizar la dirección para realizar transacciones, etc.
# Por ejemplo, imprimir el saldo de la cuenta
balance_wei = w3.eth.get_balance(account.address)
balance_eth = w3.from_wei(balance_wei, 'ether')
print(f"Saldo de la cuenta: {balance_eth} ETH")

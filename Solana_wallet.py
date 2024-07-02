import solana
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

# Generate a new keypair
new_account = Keypair.generate()

print("Public Key:", new_account.public_key)
print("Secret Key:", new_account.secret_key)

# Connect to the devnet cluster
client = Client("https://api.devnet.solana.com")

# Airdrop SOL to the new account
airdrop_response = client.request_airdrop(PublicKey(new_account.public_key), 1000000000)  # 1 SOL

# Confirm the transaction
client.confirm_transaction(airdrop_response["result"])

print("Airdrop successful")

# Check the wallet balance
balance = client.get_balance(PublicKey(new_account.public_key))
print("Wallet Balance:", balance["result"]["value"] / 1000000000, "SOL")

# Generate a recipient keypair
recipient = Keypair.generate()

# Create a transfer transaction
transaction = Transaction().add(
    transfer(
        TransferParams(
            from_pubkey=new_account.public_key,
            to_pubkey=recipient.public_key,
            lamports=10000000  # Transfer 0.01 SOL
        )
    )
)

# Sign and send the transaction
response = client.send_transaction(transaction, new_account)
print("Transfer successful, transaction signature:", response["result"])

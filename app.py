from flask import Flask, request, jsonify, render_template
from blockchain import Wallet, Transaction

app = Flask(__name__)

# In-memory storage for wallets and transactions
wallets = {}
transactions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wallet/new', methods=['POST'])
def new_wallet():
    wallet = Wallet()
    wallets[wallet.address] = wallet
    return jsonify({'address': wallet.address, 'balance': wallet.balance})

@app.route('/wallet/<address>', methods=['GET'])
def get_wallet(address):
    wallet = wallets.get(address)
    if wallet:
        return jsonify({'address': wallet.address, 'balance': wallet.balance})
    else:
        return jsonify({'error': 'Wallet not found'}), 404

@app.route('/transaction/send', methods=['POST'])
def send_transaction():
    data = request.get_json()
    sender_address = data['sender']
    recipient_address = data['recipient']
    try:
        amount = int(data['amount'])
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    sender_wallet = wallets.get(sender_address)
    recipient_wallet = wallets.get(recipient_address)

    if not sender_wallet or not recipient_wallet:
        return jsonify({'error': 'Sender or recipient wallet not found'}), 404

    if sender_wallet.balance < amount:
        return jsonify({'error': 'Insufficient funds'}), 400

    sender_wallet.balance -= amount
    recipient_wallet.balance += amount
    transaction = Transaction(sender_address, recipient_address, amount)
    transactions.append(transaction)

    return jsonify({'message': 'Transaction successful'})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify([vars(tx) for tx in transactions])

if __name__ == '__main__':
    app.run(debug=True)

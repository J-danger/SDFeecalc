from flask import Flask, render_template, request, jsonify
import requests
from web3 import Web3
import decimal
import json

app = Flask(__name__)

bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

if not web3.is_connected():
    raise Exception("Failed to connect to the BSC node")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    # Access the form data sent by the client
    user_input = request.form.get('inputData')

    transaction = user_input
    wei = 1000000000000000000

    try:
        # Fetch transaction 
        transaction_receipt = web3.eth.get_transaction_receipt(transaction)
        transaction_details = web3.eth.get_transaction(transaction)
    except Exception as e:
        return jsonify({'error': f"Error fetching transaction: {str(e)}"})

    # JSON Data
    transaction_Gas_Json = json.loads(Web3.to_json(transaction_receipt))['gasUsed']
    transaction_Value_Json = json.loads(Web3.to_json(transaction_details))

    # BSC fee
    transaction_Gas = transaction_Gas_Json * 0.000000005
    transaction_Value = transaction_Value_Json['value'] / wei

    # SD fee
    entering_Farm_Fee = transaction_Value * 0.01

    # PCS fee
    swap_Fee = (transaction_Value - entering_Farm_Fee) * 0.0025

    # Round swap fee to 8 decimal places
    swap_Fee = round(swap_Fee, 8)

    # Math
    total_Fee = transaction_Gas + swap_Fee + entering_Farm_Fee
    total_Farm = (transaction_Value - entering_Farm_Fee) / 2
    total_Fees_Percentage = total_Fee / transaction_Value * 100
    single_farm_fee = swap_Fee / 2

    # Prepare response
    transactionvalue = 'Transaction Value: ' + str(transaction_Value) + ' BNB'
    gasused = 'Gas Used: ' + str(transaction_Gas) + ' BNB'
    enterfee = 'Entering Farm on SimpleDefi - 0.1%: ' + str(entering_Farm_Fee) + ' BNB'
    atokenfee = 'PanCakeSwap Fee for BNB -> Token A - 0.25%: ' + f'{single_farm_fee:.{swap_dec_Len}f}' + ' BNB'
    btokenfee = 'PanCakeSwap Fee for BNB -> Token B - 0.25%: ' + f'{single_farm_fee:.{swap_dec_Len}f}' + ' BNB'
    totalswapfee = f'Swap Fee Total: {swap_Fee:.7f}' + ' BNB'
    feetotal = 'Total Fee: ' + str(total_Fee) + ' BNB'

    # Return the processed data as JSON
    return jsonify({
        'result': f'Your TXID: {transaction}',
        'transactionvalue': transactionvalue,
        'gasused': gasused,
        'enterfee': enterfee,
        'atokenfee': atokenfee,
        'btokenfee': btokenfee,
        'totalswapfee': totalswapfee,
        'feetotal': feetotal
    })


if __name__ == '__main__':
    app.run(debug=True)

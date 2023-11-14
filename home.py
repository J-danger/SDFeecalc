from flask import Flask, render_template, request
import requests
from web3 import Web3
import time
import json
import decimal
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.is_connected())

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    # Access the form data sent by the client
    user_input = request.form.get('inputData')

    # Process the input data (you can perform any calculations or logic here)
    processed_data = f'Your TXID: {user_input}'

    transaction = user_input
    count = 0
    wei = 1000000000000000000

    # # Json Data
    transaction_Gas_Json = json.loads(Web3.to_json(web3.eth.get_transaction_receipt(transaction)))['gasUsed']
    transaction_Value_Json = json.loads(Web3.to_json(web3.eth.get_transaction(transaction)))
    # BSC fee
    transaction_Gas = transaction_Gas_Json * 0.000000005
    transaction_Value = transaction_Value_Json['value'] / wei
    # SD fee
    entering_Farm_Fee = transaction_Value * .01
    # PCS fee
    swap_Fee = (transaction_Value - entering_Farm_Fee) * .0025
    # Swap fee dec length (to prevent scientific notation)
    swap_dec = decimal.Decimal(str(swap_Fee))
    swap_dec_Len = abs(swap_dec.as_tuple().exponent)
    print(abs(swap_dec.as_tuple().exponent))

    # Math
    total_Fee = transaction_Gas + swap_Fee + entering_Farm_Fee
    total_Farm = (transaction_Value - entering_Farm_Fee) / 2
    total_Fees_Percentage = total_Fee / transaction_Value * 100
    single_farm_fee_String = str(swap_Fee / 2)
    single_farm_fee = swap_Fee / 2

    # Test Prints
    print('Transaction Value:', str(transaction_Value) + ' BNB')
    print('Gas Used:', str(transaction_Gas) + ' BNB')
    print('0.1% Fee to enter Farm:', str(entering_Farm_Fee) + ' BNB of ' + str(transaction_Value) + ' BNB')
    print('0.25% Fee for Token A:', single_farm_fee_String + ' BNB of ' + str(total_Farm) + ' BNB')
    print('0.25% Fee for Token B:', single_farm_fee_String + ' BNB of ' + str(total_Farm) + ' BNB')
    print(f'Swap Fee Total: {swap_Fee:.7f}' + ' BNB')
    print('Total Fees:', str(total_Fee) + ' BNB')

    # transactionvalue = 'Transaction Value:', str(transaction_Value) + ' BNB'
    # gasused = 'Gas Used:', str(transaction_Gas) + ' BNB'
    # enterfee = '0.1% Fee to enter Farm:', str(entering_Farm_Fee) + ' BNB of ' + str(transaction_Value) + ' BNB'
    # atokenfee = '0.25% Fee for Token A:', single_farm_fee_String + ' BNB of ' + str(total_Farm) + ' BNB'
    # btokenfee = '0.25% Fee for Token B:', single_farm_fee_String + ' BNB of ' + str(total_Farm) + ' BNB'
    # totalswapfee = f'Swap Fee Total: {swap_Fee:.7f}' + ' BNB'
    # feetotal = 'Total Fees:', str(total_Fee) + ' BNB'

    transactionvalue = 'Transaction Value: ' + str(transaction_Value) + ' BNB'
    gasused = 'Gas Used: ' + str(transaction_Gas) + ' BNB'
    enterfee = 'Entering Farm on SimpleDefi - 0.1%: ' + str(entering_Farm_Fee) + ' BNB'
    atokenfee = 'PanCakeSwap Fee for BNB -> Token A - 0.25%: ' + f'{single_farm_fee:.{swap_dec_Len}f}' + ' BNB'
    btokenfee = 'PanCakeSwap Fee for BNB -> Token B - 0.25%: ' + f'{single_farm_fee:.{swap_dec_Len}f}' + ' BNB'
    totalswapfee = f'Swap Fee Total: {swap_Fee:.7f}' + ' BNB'
    feetotal = 'Total Fee ' + str(total_Fee) + ' BNB'


    # Return the processed data as JSON (you can customize the response as needed)
    return {'result': processed_data, 'transactionvalue': transactionvalue, 'gasused': gasused, 'enterfee': enterfee, 'atokenfee': atokenfee, 'btokenfee': btokenfee, 'totalswapfee': totalswapfee, 'feetotal': feetotal}



if __name__ == '__main__':
    app.run(debug=True)

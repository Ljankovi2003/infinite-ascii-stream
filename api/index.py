from flask import Flask, jsonify
from flask_cors import CORS
import requests
import random
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Define the RPC URL
RPC_URL = "https://api.devnet.solana.com"

# List of names to append (only one name will be selected randomly)
Names = [
    "Noodles11", "Cupsey", "Kenzo", "Grandfn3", "Spuno", 
    "Trump3", "mafia", "earl", "gm6"
]

# Other possible phrases
Phrases = [
    "Pump bonding curve completed.",
    "King of the hill reached."
]

def get_latest_slot():
    """Fetch the latest slot from the Solana network."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getEpochInfo",
        "params": []
    }

    try:
        # Make the POST request to fetch the epoch info (which contains the latest slot)
        response = requests.post(RPC_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        result = response.json()

        # Check for errors in the response
        if "error" in result:
            print(f"Error retrieving epoch info: {result['error']}")
            return None

        # Extract the latest slot from the result
        epoch_info = result.get("result", {})
        if epoch_info and "absoluteSlot" in epoch_info:
            return epoch_info["absoluteSlot"]
        else:
            print("Failed to retrieve the latest slot.")
            return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def process_block_data_and_generate_strings(slot):
    """Fetches block data, extracts signatures, and generates strings for each signature."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlock",
        "params": [
            slot,
            {
                "encoding": "json",
                "maxSupportedTransactionVersion": 0,
                "transactionDetails": "full",
                "rewards": False
            }
        ]
    }

    try:
        # Make the POST request to fetch block data
        response = requests.post(RPC_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        result = response.json()

        # Check for errors in the response
        if "error" in result:
            print(f"Error retrieving block data: {result['error']}")
            return None

        block_data = result.get("result", {})

        # Extract signatures
        if block_data and 'transactions' in block_data:
            signatures = []
            for tx in block_data['transactions']:
                if 'transaction' in tx:
                    signatures.extend(tx['transaction'].get('signatures', []))

            # Generate the string for each signature
            signature_strings = []
            for sig in signatures:
                # Randomly choose a phrase to append
                phrase = random.choice(Phrases)

                # 40% chance to add name and action
                if random.random() < 0.4:
                    # Randomly choose one name from the list to append
                    name = random.choice(Names)

                    # Randomly choose whether it's a "bought" or "sold" action (50% chance for each)
                    action = random.choice(["bought", "sold"])

                    # Construct the signature string
                    signature_str = f"Analyzing and learning from transaction {sig}. {phrase} {name} {action}."
                else:
                    # If 60% chance, do not append name and action
                    signature_str = f"Analyzing and learning from transaction {sig}. {phrase}"

                signature_strings.append(signature_str)

            return signature_strings

        else:
            print(f"No transactions found in block data for Slot {slot}.")
            return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Fetches the latest slot and generates strings for transactions."""
    # Get the latest slot dynamically
    slot = get_latest_slot()
    if slot:
        print(f"Fetching data for Slot {slot}...")

        # Fetch and generate the signature strings
        signature_strings = process_block_data_and_generate_strings(slot)

        if signature_strings:
            return jsonify({"messages": signature_strings})
        else:
            return jsonify({"error": "Failed to process data for the slot."}), 400
    else:
        return jsonify({"error": "Could not retrieve the latest slot."}), 400

@app.route('/api/functions', methods=['GET'])
def get_functions():
    functions = [
        "function example1() { console.log('Example 1'); }",
        "function example2() { console.log('Example 2'); }",
        "function example3() { console.log('Example 3'); }"
    ]
    return jsonify(functions)

if __name__ == '__main__':
    app.run(debug=True)

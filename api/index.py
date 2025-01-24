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
    transactions = [
        {str(slot)}, 
    "Analyzing and learning from transaction 5s9JAXTY2bKP9GuvhYQvHt6hJh7ybrGUV5AjwzXgXT8zQUrvdK9UjCRxHbsYReW84SF1HhfYk55DFyPB3wBFvaeZ. King of the hill reached.",
    "Analyzing and learning from transaction 43QjfEudRfZ6iLk3At7uRLibCS6biAU7CYd6byCvBqatdJmWXtkwuJKH9QZp4vzBkb7ErC1KFq2t7YH5SMwwuWnA. King of the hill reached. Grandfn3 sold.",
    "Analyzing and learning from transaction tNtPFJfTdmCuLL8rwSxdwczy9yCu2euz4pETnJuoewJuo8X6JLKuqGpUNCr59oJ2J72f2r1Qs76LndWKgyoJoAx. Pump bonding curve completed.",
    "Analyzing and learning from transaction 468WYaZTyu2wXZsmshyv72SSGQTBx9MEJnQ4eieUHUN21RD78xihE9etWdPEDvibfVwa1tux7TgYyJRcjZAfQfKC. King of the hill reached. gm6 sold.",
    "Analyzing and learning from transaction 3kytgBHwAuZnibyZz27xTXCqvWBdEc3mMJtXr1PffritJUivQ9EndUjmAsYQmyVPTLUVQvgNg84k44irausCpKfN. Pump bonding curve completed.",
    "Analyzing and learning from transaction 3NNELAchJj8mLbGUEJQpVu1vq6kXKY6j9okFSYAoG2gwYGdPRUhehAqiB8iCBwNgyF8bxWkZG1CnSPCqBZSur3Yt. Pump bonding curve completed.",
    "Analyzing and learning from transaction 54VC3H2VGMvA35h9DARmpj37Cfk4JNypV4dzWM7Q5orAp3a4LyBvnW9GL1qgLAyVfP4J8Zq1k3Gtugyx6VYHRrCA. Pump bonding curve completed. Spuno bought.",
    "Analyzing and learning from transaction 2dxcytiq6oA3mFTTcVA2qLaP71uiKT5SM1sMSpimpY836xe5HJi8V1VgqP48h6jMck9NyQgjfinkJiQDcK6HDA4J. Pump bonding curve completed.",
    "Analyzing and learning from transaction YeFrmww71wjGDA16V8trKm5D2gsBXXc5V5tTr7SZBfqD1hn7tU8ypib7Dz9ESFDBRFtYx9fo3HxTNUMcd2E29u4. King of the hill reached. Kenzo sold.",
    "Analyzing and learning from transaction 62eZJ3kkNCPNykurHM3VNVVQy7SzfqRCiv5DnBWtcTZAx2MFjREziMqhWx8aMu9iXqxXA9AsPtUnrDUjHeiMuT5. Pump bonding curve completed.",
    "Analyzing and learning from transaction 4MMA7YTSDSjJ7y8cqRi6Tpxs4RjY17QzAH7hWogaVr46TPWRF1dbmwuiwUnDJrAAntRzjJxHz2maWdgzNHhLRNfB. Pump bonding curve completed. mafia sold.",
    "Analyzing and learning from transaction 4AgF2VsEdiS1k9dUc4jWfggbYePWy3DM71PYxuJ8iSNNVLPJHXbaRdmRvvQSaBC4yeAcRw5rXFsXTpPYoDqpV7Sx. Pump bonding curve completed. Cupsey sold.",
    "Analyzing and learning from transaction 55AzABFH8m5UqikyUDGjd9R4L9tNDxcsqKZmfiztrUyKoCjMNZe5Vme2ZwiS59Smf7ktcNbDMBcPvYU3PeudXFG2. King of the hill reached.",
    "Analyzing and learning from transaction YGNVuNANcg2iyfqAvLSuQ7zPKNjYj6zQpBdBg8o2dh1ebSm2gqroY8YhGLyAzujTeakqfciuBrhjcvR4m9KgYTB. Pump bonding curve completed. earl sold.",
    "Analyzing and learning from transaction NdRmofYpvkpbwuoqxMYvedg3tWFjizAcPvfUCb8PxbtntmqHp9hfKwCkZSByyzCnJYXsbUE8ynCg6KcdUNNW3cY. Pump bonding curve completed. Spuno bought.",
    "Analyzing and learning from transaction 8Jpz2rDukrfdaHH7VeufaRv5fFTummA4wjz8oNs9JzasskMfbV9wgdjEdMSRScreAKJ9qP4XdJzdWbCsvytdUF3. King of the hill reached.",
    "Analyzing and learning from transaction 51fuK39YpD8DJLaQWZoyYicS7LNq8qErYxiwACaBJPvki8NACbxE7MxJYVhC6fozLX7xQHPzkkMUxsB2JMLCEY6. King of the hill reached.",
    "Analyzing and learning from transaction 4pTadbsvH8jPa8Us4zfB8rfJxCEg4qaF4VUhtax1AShnTsTdvUvsB3AbZNSxayG4U34zadVLoL5mQfxcj4T4eG9W. Pump bonding curve completed.",
    "Analyzing and learning from transaction 3Gz77rADUWnioH4GWicHkAVex32XH9QpFvEyVg8ntLt9Fe6vTAsXsDXtL3Awo4QncfBguASh5FDMbTahbjgPXWJk. Pump bonding curve completed.",
    "Analyzing and learning from transaction 3SFJLACrJJ7ExMxbbahAJ43SLVBj2qyAbwtUYUMb9iRJvQa7EuEknQJFiMJkNzpShF8PuLfGVJrGP7iEePAdENAV. Pump bonding curve completed.",
    "Analyzing and learning from transaction 5fcSCvzFrDiBYNScPWN7eyrQteFLg4H1j5vzdakQN1GbpwTVVhB1Sa9WD1foFrXaM3wFLXuEQmmregtLWpH4bofq. Pump bonding curve completed. mafia bought.",
    "Analyzing and learning from transaction 51yT42RqD9Xwq9LennidCd7Gtz9cFffgQiNncbhLQEADHn4Pe2xotNKsoAozhEzPYyDDz2z6wNiADjWXDvZtbTov. King of the hill reached.",
    "Analyzing and learning from transaction 4Z67ty6igUcq27R8JKGocQVrv5LHHtAbkccBc4eUqekJLrQLd26Wk6jkfoap6BmXT1ayiF8Ggu64tpD2h3UcFHTZ. Pump bonding curve completed. earl bought.",
    "Analyzing and learning from transaction 3FnqdUVbhCHFjXDhumsM2Gx3XHDGt5mgXRTBjUc7CjLUEJGrBQ7TusSgLGifNR4tF4CoCdTTD9skBS1aCTgANpvv. King of the hill reached.",
    "Analyzing and learning from transaction 2R1jQyh2imB4x5ZuJxqPvC4pjLoJguuVLnWMrvuJFUP8hsA6JCcfZDgbjxjo13nbCyi2EdMa9BvWhGjcyU6uusfc. King of the hill reached.",
    "Analyzing and learning from transaction LFUSKgXsSCTxjStvtr4yFeSBaoYVArj6QPuFakaPspomEiTvLLfvxQuavFpBXAD8RiQWzeBSAeZnK69WArqvfqm. Pump bonding curve completed.",
    "Analyzing and learning from transaction 4mxXFLCBmt8nZmm1vckdnGo5kFkE5RzruZsL6WmACHrTtWY7zJShvbVRabefSEC6Zdbkz1pS9RTmVZbUWqyGkCwJ. King of the hill reached. gm6 sold."]
    
    return jsonify(transactions)

@app.route('/api/functions', methods=['GET'])
def get_functions():
    transactions = [
    "Analyzing and learning from transaction 5s9JAXTY2bKP9GuvhYQvHt6hJh7ybrGUV5AjwzXgXT8zQUrvdK9UjCRxHbsYReW84SF1HhfYk55DFyPB3wBFvaeZ. King of the hill reached.",
    "Analyzing and learning from transaction 43QjfEudRfZ6iLk3At7uRLibCS6biAU7CYd6byCvBqatdJmWXtkwuJKH9QZp4vzBkb7ErC1KFq2t7YH5SMwwuWnA. King of the hill reached. Grandfn3 sold.",
    "Analyzing and learning from transaction tNtPFJfTdmCuLL8rwSxdwczy9yCu2euz4pETnJuoewJuo8X6JLKuqGpUNCr59oJ2J72f2r1Qs76LndWKgyoJoAx. Pump bonding curve completed.",
    "Analyzing and learning from transaction 468WYaZTyu2wXZsmshyv72SSGQTBx9MEJnQ4eieUHUN21RD78xihE9etWdPEDvibfVwa1tux7TgYyJRcjZAfQfKC. King of the hill reached. gm6 sold.",
    "Analyzing and learning from transaction 3kytgBHwAuZnibyZz27xTXCqvWBdEc3mMJtXr1PffritJUivQ9EndUjmAsYQmyVPTLUVQvgNg84k44irausCpKfN. Pump bonding curve completed.",
    "Analyzing and learning from transaction 3NNELAchJj8mLbGUEJQpVu1vq6kXKY6j9okFSYAoG2gwYGdPRUhehAqiB8iCBwNgyF8bxWkZG1CnSPCqBZSur3Yt. Pump bonding curve completed.",
    "Analyzing and learning from transaction 54VC3H2VGMvA35h9DARmpj37Cfk4JNypV4dzWM7Q5orAp3a4LyBvnW9GL1qgLAyVfP4J8Zq1k3Gtugyx6VYHRrCA. Pump bonding curve completed. Spuno bought.",
    "Analyzing and learning from transaction 2dxcytiq6oA3mFTTcVA2qLaP71uiKT5SM1sMSpimpY836xe5HJi8V1VgqP48h6jMck9NyQgjfinkJiQDcK6HDA4J. Pump bonding curve completed.",
    "Analyzing and learning from transaction YeFrmww71wjGDA16V8trKm5D2gsBXXc5V5tTr7SZBfqD1hn7tU8ypib7Dz9ESFDBRFtYx9fo3HxTNUMcd2E29u4. King of the hill reached. Kenzo sold.",
    "Analyzing and learning from transaction 62eZJ3kkNCPNykurHM3VNVVQy7SzfqRCiv5DnBWtcTZAx2MFjREziMqhWx8aMu9iXqxXA9AsPtUnrDUjHeiMuT5. Pump bonding curve completed.",
    "Analyzing and learning from transaction 4MMA7YTSDSjJ7y8cqRi6Tpxs4RjY17QzAH7hWogaVr46TPWRF1dbmwuiwUnDJrAAntRzjJxHz2maWdgzNHhLRNfB. Pump bonding curve completed. mafia sold.",
    "Analyzing and learning from transaction 4AgF2VsEdiS1k9dUc4jWfggbYePWy3DM71PYxuJ8iSNNVLPJHXbaRdmRvvQSaBC4yeAcRw5rXFsXTpPYoDqpV7Sx. Pump bonding curve completed. Cupsey sold.",
    "Analyzing and learning from transaction 55AzABFH8m5UqikyUDGjd9R4L9tNDxcsqKZmfiztrUyKoCjMNZe5Vme2ZwiS59Smf7ktcNbDMBcPvYU3PeudXFG2. King of the hill reached.",
    "Analyzing and learning from transaction YGNVuNANcg2iyfqAvLSuQ7zPKNjYj6zQpBdBg8o2dh1ebSm2gqroY8YhGLyAzujTeakqfciuBrhjcvR4m9KgYTB. Pump bonding curve completed. earl sold.",
    "Analyzing and learning from transaction NdRmofYpvkpbwuoqxMYvedg3tWFjizAcPvfUCb8PxbtntmqHp9hfKwCkZSByyzCnJYXsbUE8ynCg6KcdUNNW3cY. Pump bonding curve completed. Spuno bought.",
    "Analyzing and learning from transaction 8Jpz2rDukrfdaHH7VeufaRv5fFTummA4wjz8oNs9JzasskMfbV9wgdjEdMSRScreAKJ9qP4XdJzdWbCsvytdUF3. King of the hill reached.",
    "Analyzing and learning from transaction 51fuK39YpD8DJLaQWZoyYicS7LNq8qErYxiwACaBJPvki8NACbxE7MxJYVhC6fozLX7xQHPzkkMUxsB2JMLCEY6. King of the hill reached.",
    "Analyzing and learning from transaction 4pTadbsvH8jPa8Us4zfB8rfJxCEg4qaF4VUhtax1AShnTsTdvUvsB3AbZNSxayG4U34zadVLoL5mQfxcj4T4eG9W. Pump bonding curve completed.",
    "Analyzing and learning from transaction 3Gz77rADUWnioH4GWicHkAVex32XH9QpFvEyVg8ntLt9Fe6vTAsXsDXtL3Awo4QncfBguASh5FDMbTahbjgPXWJk. Pump bonding curve completed.",
    "Analyzing and learning from transaction 3SFJLACrJJ7ExMxbbahAJ43SLVBj2qyAbwtUYUMb9iRJvQa7EuEknQJFiMJkNzpShF8PuLfGVJrGP7iEePAdENAV. Pump bonding curve completed.",
    "Analyzing and learning from transaction 5fcSCvzFrDiBYNScPWN7eyrQteFLg4H1j5vzdakQN1GbpwTVVhB1Sa9WD1foFrXaM3wFLXuEQmmregtLWpH4bofq. Pump bonding curve completed. mafia bought.",
    "Analyzing and learning from transaction 51yT42RqD9Xwq9LennidCd7Gtz9cFffgQiNncbhLQEADHn4Pe2xotNKsoAozhEzPYyDDz2z6wNiADjWXDvZtbTov. King of the hill reached.",
    "Analyzing and learning from transaction 4Z67ty6igUcq27R8JKGocQVrv5LHHtAbkccBc4eUqekJLrQLd26Wk6jkfoap6BmXT1ayiF8Ggu64tpD2h3UcFHTZ. Pump bonding curve completed. earl bought.",
    "Analyzing and learning from transaction 3FnqdUVbhCHFjXDhumsM2Gx3XHDGt5mgXRTBjUc7CjLUEJGrBQ7TusSgLGifNR4tF4CoCdTTD9skBS1aCTgANpvv. King of the hill reached.",
    "Analyzing and learning from transaction 2R1jQyh2imB4x5ZuJxqPvC4pjLoJguuVLnWMrvuJFUP8hsA6JCcfZDgbjxjo13nbCyi2EdMa9BvWhGjcyU6uusfc. King of the hill reached.",
    "Analyzing and learning from transaction LFUSKgXsSCTxjStvtr4yFeSBaoYVArj6QPuFakaPspomEiTvLLfvxQuavFpBXAD8RiQWzeBSAeZnK69WArqvfqm. Pump bonding curve completed.",
    "Analyzing and learning from transaction 4mxXFLCBmt8nZmm1vckdnGo5kFkE5RzruZsL6WmACHrTtWY7zJShvbVRabefSEC6Zdbkz1pS9RTmVZbUWqyGkCwJ. King of the hill reached. gm6 sold."]
    
    return jsonify(transactions)

if __name__ == '__main__':
    app.run()

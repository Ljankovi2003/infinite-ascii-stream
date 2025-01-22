from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/functions', methods=['GET'])
def get_functions():
    functions = [
        "function example1() { console.log('Example 1'); }",
        "function example2() { console.log('Example 2'); }",
        "function example3() { console.log('Example 3'); }"
    ]
    return jsonify(functions)

if __name__ == "__main__":
    app.run()

from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route("/api/insert_rows", methods=["POST"])
def insert_rows():
    if not request.data:
        return jsonify({"error": "No data provided"})
    data = json.loads(request.data)
    # insert data into the postgresql database


app.run(debug=True)

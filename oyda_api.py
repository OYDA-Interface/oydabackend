from flask import Flask, request, jsonify
import json
import psycopg2
# import pg8000.native

app = Flask(__name__)




@app.route("/api/createTable", methods=["POST"])
def create_table():
    if not request.data:
        return jsonify({"error":"No data provided"}),400
    data = json.loads(request.data)

    tableName = data.get('tableName')
    columns = data.get('columns')

    if not tableName or not columns:
        return jsonify({"error":"No table name or columns specified"}), 400
    

@app.route("/api/insert_rows", methods=["POST"])
def insert_rows():
    if not request.data:
        return jsonify({"error": "No data provided"})
    data = json.loads(request.data)
    # insert data into the postgresql database


# if __name__ == '__main__':
#     app.run(debug=True)

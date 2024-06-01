from flask import Flask, request, jsonify
import json
import pg8000.native

app = Flask(__name__)

@app.route("/api/setOydabase", methods=["POST"])
def set_oydabase():
    if not request.data:
        return jsonify({"error": "No data provided"}), 400
    try:
        data = json.loads(request.data)
        print(data)

        host = data.get('host')
        port = data.get('port', 5432) 
        database = data.get('database')
        user = data.get('user')
        password = data.get('password')

        if not all([host, database, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400
        
        # Establish a connection to the PostgreSQL database
        conn = pg8000.native.Connection(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            ssl_context=False
        )
        # Close the connection after testing
        conn.close()

        return jsonify({"message": "Connection successful"}), 200

    except pg8000.Error as e:
        return jsonify({"error": f"Database connection failed: {e}"}), 500

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400



@app.route("/api/insert_rows", methods=["POST"])
def insert_rows():
    if not request.data:
        return jsonify({"error": "No data provided"})
    data = json.loads(request.data)
    # insert data into the postgresql database


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import json
import psycopg2
# import pg8000.native

app = Flask(__name__)

@app.route("/api/setOydabase", methods=["POST"])
def set_oydabase():
    if not request.data:
        return jsonify({"error":"No data provided"}), 400
    try:
        data = json.loads(request.data)
        print(data)

        host = data.get('host')
        port = data.get('port', 5432) 
        dbname = data.get('dbname')
        user = data.get('user')
        password = data.get('password')  

        if not all([host, dbname, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400
        
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

        conn.close()

        return jsonify({"message":"Connection successful"}), 200
    
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"Database connection failed: {e}"}), 500



@app.route("/api/insert_rows", methods=["POST"])
def insert_rows():
    if not request.data:
        return jsonify({"error": "No data provided"})
    data = json.loads(request.data)
    # insert data into the postgresql database


if __name__ == '__main__':
    app.run(debug=True)

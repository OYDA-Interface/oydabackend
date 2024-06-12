from flask import Blueprint, request, jsonify
import psycopg2 # type: ignore
import json

connections_bp = Blueprint("connection_manager", __name__)

@connections_bp.route("/api/setOydabase", methods=["POST"])
def set_oydabase():
    if not request.data:
        return jsonify({"error":"No data provided"}), 400
    try:
        data = json.loads(request.data)
        # print(data)

        host = data.get('host')
        port = data.get('port', 5432) 
        oydaBase = data.get('oydaBase')
        user = data.get('user')
        password = data.get('password')  

        if not all([host, oydaBase, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400
        
        conn = psycopg2.connect(dbname=oydaBase, user=user, password=password, host=host, port=port)

        conn.close()

        return jsonify({"message":"Oydabase set successfully"}), 200
    
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f" Error connecting to the Oydabase: {e}"}), 500
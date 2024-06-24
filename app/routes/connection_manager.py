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

        host = data.get('host')
        port = data.get('port', 5432) 
        oydaBase = data.get('oydaBase')
        user = data.get('user')
        password = data.get('password')  

        if not all([host, oydaBase, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400
        
        conn = psycopg2.connect(dbname=oydaBase, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'dependencies'
        );
        """
        )
        exists = cursor.fetchone()[0]

        if exists:
            return jsonify({"message":"Oydabase set successfully: Dependencies exist"}), 200
        else:
            cursor.execute("""
            CREATE TABLE dependencies (
                name VARCHAR(255) NOT NULL,
                version VARCHAR(255) NOT NULL
            );
            """)
            conn.commit()
            message = "Connected to Oydabase @ " + host + ":" + port + "/" + oydaBase + ".: Dependencies table created"

        cursor.close()
        conn.close()

        return jsonify({"message":message}), 200
    
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"{e}"}), 500
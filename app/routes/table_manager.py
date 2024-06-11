from flask import Blueprint, request, jsonify
import psycopg2
import json

table_manager_bp = Blueprint("table_manager", __name__)

@table_manager_bp.route("/api/selectTable", methods=["POST"])
def selectTable():
  if not request.data:
    return jsonify({"error":"No data provided"}), 400
  try:
    data = json.loads(request.data)
    host = data.get('host')
    port = data.get('port', 5432) 
    oydaBase = data.get('oydaBase')
    user = data.get('user')
    password = data.get('password')
    table_name = data.get('table_name')

    if not all([host, oydaBase, user, password, table_name]):
      return jsonify({"error": "Missing required connection parameters or table name"}), 400

    conn = psycopg2.connect(dbname=oydaBase, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    result = []
    for row in rows:
      result.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return jsonify(result), 200

  except psycopg2.DatabaseError as e:
      return jsonify({"error": f"Database error: {e}"}), 500
  except Exception as e:
      return jsonify({"error": f"Error: {e}"}), 500


@table_manager_bp.route("/api/dropTable", methods=["POST"])
def dropTable():
  if not request.data:
    return jsonify({"error":"No data provided"}), 400
  try:
    data = json.loads(request.data)
    host = data.get('host')
    port = data.get('port', 5432) 
    oydaBase = data.get('oydaBase')
    user = data.get('user')
    password = data.get('password')
    table_name = data.get('table_name')

    if not all([host, oydaBase, user, password, table_name]):
      return jsonify({"error": "Missing required connection parameters or table name"}), 400

    conn = psycopg2.connect(dbname=oydaBase, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    query = f"DROP TABLE {table_name};"
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": f"Table {table_name} dropped successfully"}), 200

  except psycopg2.DatabaseError as e:
      return jsonify({"error": f"Database error: {e}"}), 500
  except Exception as e:
      return jsonify({"error": f"Error: {e}"}), 500

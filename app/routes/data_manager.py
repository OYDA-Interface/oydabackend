from flask import Blueprint, request, jsonify
import psycopg2
import json

data_bp = Blueprint("data_manager", __name__)

# @data_bp.route("/api/selectRow", methods=["POST"])
# def selectRow():
#   if not request.data:
#     return jsonify({"error":"No data provided"}), 400
#   try: 
#     data = json.loads(request.data)
#     host = data.get('host')
#     port = data.get('port', 5432)
#     oydaBase = data.get('oydaBase')
#     user = data.get('user')
#     password = data.get('password')
#     table_name = data.get('table_name')

#     if not all([host, oydaBase, user, password, table_name]):
#       return jsonify({"error": "Missing required connection parameters or table name"}), 400
    
#     conn = psycopg2.connect(dbname=oydaBase, user=user, password=password, host=host, port=port)
#     cursor = conn.cursor()

    

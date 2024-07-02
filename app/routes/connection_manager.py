from flask import Blueprint, request, jsonify
import psycopg2  # type: ignore
import json, random
import requests

import app.utilities as utils

connections_bp = Blueprint("connection_manager", __name__)

@connections_bp.route("/api/set_oydabase", methods=["POST"])
def set_oydabase():
    """
    The function `set_oydabase` establishes a connection to a oydabase, creates dependency
    and dev tables if they don't exist, and manages developer keys for a given username.

    :return: Returns a JSON response with a message indicating the successful connection to the
    oydabase and the creation of the dependencies table. The response also includes the
    developer key for the given username.
    """
    if not request.data:
        return jsonify({"error": "No data provided"}), 400
    try:
        data = json.loads(request.data)

        host = data.get("host")
        port = data.get("port", 5432)
        oydaBase = data.get("oydaBase")
        user = data.get("user")
        password = data.get("password")

        if not all([host, oydaBase, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400

        conn = psycopg2.connect(
            dbname=oydaBase, user=user, password=password, host=host, port=port
        )
        cursor = conn.cursor() 
        
        # Check for dependencies table
        if not utils.check_table_exists(cursor, "dependencies"):
            utils.create_dependencies_table(cursor)
            conn.commit()
            message = f"Connected to Oydabase @ {host}:{port}/{oydaBase}. Dependencies table created"
        else:
            message = f"Connected to Oydabase @ {host}:{port}/{oydaBase}: Dependencies exist"

        # Check for devs table
        if not utils.check_table_exists(cursor, "devs"):
            utils.create_devs_table(cursor)
            conn.commit()
        
        # Handle developer keys
        dev_key = utils.get_or_create_dev_key(cursor, user)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": message, "dev_key": dev_key}), 200
    
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"{e}"}), 500


@connections_bp.route("/api/get_dependencies", methods=["POST"])
def get_dependencies():
    """
    The function `get_dependencies` retrieves the dependencies from the dependencies table in the oydabase.
    
    :return: Returns a JSON response with the dependencies from the oydabase if they exist.
    """
    if not request.data:
        return jsonify({"error": "No data provided"}), 400
    try:
        data = json.loads(request.data)
        
        host = data.get("host")
        port = data.get("port", 5432)
        oydaBase = data.get("oydaBase")
        user = data.get("user")
        password = data.get("password")
        
        if not all([host, oydaBase, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400
        
        conn = psycopg2.connect(
            dbname=oydaBase, user=user, password=password, host=host, port=port
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, version FROM dependencies")
        dependencies = cursor.fetchall()
        
        if not dependencies:
            return jsonify({"dependencies": "No dependencies found"}), 200
        
        cursor.close()
        conn.close()
        
        dependencies_list = [f"{name}: {version}" for name, version in dependencies]
        
        return jsonify({"dependencies": dependencies_list}), 200
    
    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"{e}"}), 500
    
    
@connections_bp.route("/api/add_dependency", methods=["POST"])
def add_dependency():
    """
    The function `add_dependency` adds a package to the dependencies table in the oydabase.
    
    :return: Returns a JSON response with a message indicating the successful addition of the package or its version if it already exists.
    """
    if not request.data:
        return jsonify({"error": "No data provided"}), 400
    try:
        data = json.loads(request.data)
        
        host = data.get("host")
        port = data.get("port", 5432)
        oydaBase = data.get("oydaBase")
        user = data.get("user")
        password = data.get("password")
        package_name = data.get("package_name")
        
        if not all([host, oydaBase, user, password]):
            return jsonify({"error": "Missing required connection parameters"}), 400
        
        conn = psycopg2.connect(
            dbname=oydaBase, user=user, password=password, host=host, port=port
        )
        
        cursor = conn.cursor()
        
        cursor.execute('SELECT version FROM dependencies WHERE name = %s', (package_name,))
        result = cursor.fetchone()
        
        if result:
            package_version = result[0]
            return jsonify({'message': f'Package {package_name} already exists with version {package_version}'}), 200
        else:
            response = requests.get(f'https://pub.dev/api/packages/{package_name}')
            if response.status_code == 200:
                package_info = response.json()
                package_version = package_info['latest']['version']
                
                cursor.execute('INSERT INTO dependencies (name, version) VALUES (%s, %s)', (package_name, package_version))
                conn.commit()
                
                return jsonify({'message': f'Package {package_name} added with version {package_version}'}), 201
            else:
                return jsonify({'error': f'Failed to fetch package {package_name} from pub.dev'}), 400

    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"{e}"}), 500

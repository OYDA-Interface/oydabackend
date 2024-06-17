from flask import Blueprint, request, jsonify
import psycopg2  # type: ignore
import json

data_bp = Blueprint("data_manager", __name__)


@data_bp.route("/api/selectRows", methods=["POST"])
def selectRows():
    if not request.data:
        return jsonify({"error": "No data provided"}), 400

    try:
        data = json.loads(request.data)

        host = data.get("host")
        port = data.get("port", 5432)
        oydaBase = data.get("oydaBase")
        user = data.get("user")
        password = data.get("password")
        table_name = data.get("table_name")
        conditions = data.get("conditions")

        if not all([host, oydaBase, user, password, table_name]):
            return (
                jsonify(
                    {"error": "Missing required connection parameters or table name"}
                ),
                400,
            )

        conn = psycopg2.connect(
            dbname=oydaBase, user=user, password=password, host=host, port=port
        )
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"

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


@data_bp.route("/api/selectColumns", methods=["POST"])
def selectColumns():
    if not request.data:
        return jsonify({"error": "No data provided"}), 400

    try:
        data = json.loads(request.data)

        host = data.get("host")
        port = data.get("port", 5432)
        oydaBase = data.get("oydaBase")
        user = data.get("user")
        password = data.get("password")
        table_name = data.get("table_name")
        columns = data.get("columns")
        conditions = data.get("conditions")

        if not all([host, oydaBase, user, password, table_name, columns]):
            return (
                jsonify(
                    {
                        "error": "Missing required connection parameters, table name, or columns"
                    }
                ),
                400,
            )

        conn = psycopg2.connect(
            dbname=oydaBase, user=user, password=password, host=host, port=port
        )
        cursor = conn.cursor()

        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"

        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        result = []
        for row in rows:
            result.append(dict(zip(column_names, row)))

        cursor.close()
        conn.close()

        return jsonify(result), 200

    except psycopg2.DatabaseError as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500


@data_bp.route("/api/insert_row", methods=["POST"])
def insert_rows():
    if not request.data:
        return jsonify({"error": "No data provided"})
    data = json.loads(request.data)

    host = data.get("host")
    port = data.get("port", 5432)
    dbname = data.get("dbname")
    user = data.get("user")
    password = data.get("password")
    table = data.get("table")
    row = data.get("row")

    if not all([host, dbname, user, password, table, row]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        cur = conn.cursor()

        columns = ", ".join(row.keys())
        values = ", ".join([f"'{v}'" for v in row.values()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        cur.execute(query)
        conn.commit()
        conn.close()

        return jsonify({"message": "Row inserted successfully"}), 200

    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"Database connection failed: {e}"}), 500


@app.route("api/update_row")
def update_row():
    if not request.data:
        return jsonify({"error": "No data provided"}), 400
    data = json.loads(request.data)

    host = data.get("host")
    port = data.get("port", 5432)
    dbname = data.get("dbname")
    user = data.get("user")
    password = data.get("password")
    table = data.get("table")
    row = data.get("row")
    condition = data.get("condition")

    if not all([host, dbname, user, password, table, row, condition]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        cur = conn.cursor()

        columns = ", ".join([f"{k} = '{v}'" for k, v in row.items()])
        condition = " AND ".join([f"{k} = '{v}'" for k, v in condition.items()])
        query = f"UPDATE {table} SET {columns} WHERE {condition}"
        cur.execute(query)
        conn.commit()
        conn.close()

        return jsonify({"message": "Row updated successfully"}), 200

    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"Database connection failed: {e}"}), 500

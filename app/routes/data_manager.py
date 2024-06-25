from flask import Blueprint, request, jsonify
import psycopg2  # type: ignore
import json

data_bp = Blueprint("data_manager", __name__)


@data_bp.route("/api/selectRows", methods=["POST"])
def selectRows():
    """
    The `selectRows` function retrieves rows from a PostgreSQL database table based on provided
    connection parameters and conditions.
    :return: Returns a JSON response containing the result of the SQL query
    executed on a PostgreSQL database table based on the provided parameters. The result includes the
    rows fetched from the table with column names as keys in a list of dictionaries.
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
        return jsonify({"error": f"{e}"}), 500
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


@data_bp.route("/api/selectColumns", methods=["POST"])
def selectColumns():
    """
    The `selectColumns` function retrieves specific columns from a database table based on provided
    parameters and conditions.
    :return: Returns a JSON response containing the result of selecting
    specific columns from a database table based on the provided parameters. The response includes the
    data fetched from the database table in a structured format.
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
        return jsonify({"error": f"{e}"}), 500
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


@data_bp.route("/api/insert_row", methods=["POST"])
def insert_rows():
    """
    The `insert_rows` function inserts a row of data into a specified table in a PostgreSQL database
    based on the provided parameters.
    :return: Returns a JSON response with a success message if the row was
    inserted successfully, or an error message if there was an issue with the database connection.
    """
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


@data_bp.route("/api/update_row")
def update_row():
    """
    The function `update_row` updates a row in a PostgreSQL database table based on provided data and
    conditions.
    :return: Returns a JSON response with a success message if the row update
    operation is successful. If there is an error or exception during the database connection or update
    process, it returns a JSON response with an error message.
    """
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

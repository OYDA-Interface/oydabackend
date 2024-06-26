from flask import Blueprint, request, jsonify
import psycopg2  # type: ignore
import json, random

connections_bp = Blueprint("connection_manager", __name__)


def generate_unique_dev_key(cursor):
    """
    This is a helper function that generates a unique developer key by randomly selecting a number
    and checking if it already exists in a database table.

    :param cursor: The `cursor` parameter is a database object to interact with a database. I
    :return: Returns a unique developer key that is not already present in the database table `devs`.
    """
    while True:
        dev_key = random.randint(100000, 999999)
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM devs WHERE dev_key = %s)", (dev_key,)
        )
        if not cursor.fetchone()[0]:
            return dev_key


@connections_bp.route("/api/setOydabase", methods=["POST"])
def set_oydabase():
    """
    The function `set_oydabase` establishes a connection to a PostgreSQL database, creates dependency
    and dev tables if they don't exist, and manages developer keys for a given username.

    :return: Returns a JSON response with a message indicating the successful connection to the
    PostgreSQL database and the creation of the dependencies table. The response also includes the
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

        # Query to check if dependencies table exists
        cursor.execute(
            """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'dependencies'
        );
        """
        )
        dependencies_table = cursor.fetchone()[0]

        if dependencies_table:
            return (
                jsonify({"message": "Oydabase set successfully: Dependencies exist"}),
                200,
            )
        else:
            cursor.execute(
                """
            CREATE TABLE dependencies (
                name VARCHAR(255) NOT NULL,
                version VARCHAR(255) NOT NULL
            );
            """
            )
            conn.commit()
            message = (
                "Connected to Oydabase @ "
                + host
                + ":"
                + port
                + "/"
                + oydaBase
                + ".: Dependencies table created"
            )

        # query to check if devs table exists
        cursor.execute(
            """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'devs'
        );
        """
        )

        devs_table = cursor.fetchone()[0]

        if not devs_table:
            cursor.execute(
                """
                CREATE TABLE devs (
                    username VARCHAR(255) NOT NULL,
                    dev_key INTEGER NOT NULL
                );
                """
            )
            conn.commit()

        # Check if the username is in the devs table
        cursor.execute("SELECT dev_key FROM devs WHERE username = %s", (user,))
        result = cursor.fetchone()

        if result:
            dev_key = result[0]
        else:
            dev_key = generate_unique_dev_key(cursor)
            cursor.execute(
                "INSERT INTO devs (username, dev_key) VALUES (%s, %s)", (user, dev_key)
            )
            conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": message, "dev_key": dev_key}), 200

    except (Exception, psycopg2.DatabaseError) as e:
        return jsonify({"error": f"{e}"}), 500

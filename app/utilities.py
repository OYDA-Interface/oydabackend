import random


def check_table_exists(cursor, table_name):
    """
    This is a helper function that checks if a table exists in the oydabase.
    
    :param cursor: The `cursor` parameter is a database object to interact with a database.
    :param table_name: The `table_name` parameter is a string that represents the name of the table.
    :return: Returns a boolean value indicating whether the table exists in the oydabase.
    """
    cursor.execute(
        f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = '{table_name}'
        );
        """
    )
    return cursor.fetchone()[0]

def create_dependencies_table(cursor):
    """
    This is a helper function that creates a `dependencies` table in a oydabase.
    
    :param cursor: The `cursor` parameter is a database object to interact with a database.
    """
    cursor.execute(
        """
        CREATE TABLE dependencies (
            name VARCHAR(255) NOT NULL,
            version VARCHAR(255) NOT NULL
        );
        """
    )

def create_devs_table(cursor):
    """
    This is a helper function that creates a `devs` table in a oydabase.
    
    :param cursor: The `cursor` parameter is a database object to interact with a database.
    """
    cursor.execute(
        """
        CREATE TABLE devs (
            username VARCHAR(255) NOT NULL,
            dev_key INTEGER NOT NULL
        );
        """
    )

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
        
def get_or_create_dev_key(cursor, username):
    """
    This is a helper function that retrieves a developer key for a given username from the database
    table `devs`. If the username is not present in the table, a new developer key is generated and
    inserted into the table.
    
    :param cursor: The `cursor` parameter is a database object to interact with a database.
    :param username: The `username` parameter is a string that represents the username.
    :return: Returns a developer key for a given username.
    """
    cursor.execute("SELECT dev_key FROM devs WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        dev_key = generate_unique_dev_key(cursor)
        cursor.execute("INSERT INTO devs (username, dev_key) VALUES (%s, %s)", (username, dev_key))
        return dev_key
# oydabackend

oydabackend is a Flask-based backend application designed to work with oydadb to manage oydabase operations for a specific project. It utilizes PostgreSQL for data storage and manipulation, facilitated by the psycopg2 library.

## Features

- **Connection Management**: Establish and manage connections to the PostgreSQL database.
- **Data Management**: Perform CRUD operations on the database. This includes selecting rows or columns, inserting new rows, and updating existing rows in the database.
- **Table Manager**: Perform table operations on the database.


- POST `/api/set_oydabase`: Configure the database connection.
- POST `/api/get_dependencies`: Retrieve the dependencies from the PostgreSQL database.
- POST `/api/add_dependency`: Add a new dependency to the dependency table of the database.
- POST `/api/select_rows`: Retrieve specific rows from a table.
- POST `/api/select_columns`: Retrieve specific columns from a table.
- POST `/api/insert_row`: Insert a new row into a table.
- POST `/api/update_row`: Update an existing row in a table.
- POST `/api/select_table`: Retrieve the entire table data.
- POST `/api/table_exists`: Check if a table exists in the database.
- POST `/api/drop_table`: Drop a table from the database.

For more detailed information on the endpoints and their usage, refer to the individual route handlers in the [`app/routes`](app/routes) directory.

## Deployment

This project includes a GitHub Actions workflow for continuous integration and deployment to Azure Web App. The workflow is defined in [`.github/workflows/main_oydabackend.yml`](.github/workflows/main_oydabackend.yml) and includes steps for setting up Python, installing dependencies, packaging the application, and deploying it to Azure.





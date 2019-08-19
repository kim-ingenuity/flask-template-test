# FLASK VARIABLES
export SECRET_KEY='YOUR_SECRET_KEY'
export FLASK_ENV='dev'

# SQLALCHEMY VARIABLES
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export SQLALCHEMY_SESSION_NO_AUTOFLUSH=False

# DATABASE CONNECTION
# For the database connection, use either the SQLALCHEMY_DATABASE_URI to set the
# database URI, or the CONN_* variables. If both are used, only the SQLALCHEMY_DATABASE_URI
# variable will be used
# Use either CONN_DATABASE or CONN_QUERY. They shouldn't be used at the same time

# export SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'

export CONN_DRIVERNAME='postgresql+psycopg2'
export CONN_HOST='localhost'
export CONN_PORT=5432
export CONN_USERNAME='user'
export CONN_PASSWORD='user'
# export CONN_DATABASE=''
export CONN_QUERY={"service_name": "user.db.com", "mode": 2}
export DATABASE_SCHEMA={"schema": "public"}

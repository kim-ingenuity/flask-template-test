# FLASK VARIABLES
export SECRET_KEY='YOUR_SECRET_KEY'
export FLASK_ENV='dev'

# SQLALCHEMY VARIABLES
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export SQLALCHEMY_SESSION_NO_AUTOFLUSH=False

# LOGGING
# Options: critical, error, warning, info, debug, notset
export LOGGING_LEVEL='debug'

# DEPLOYMENT
export UPDATE_DATABASE_TABLES_DURING_CONTAINER_RUN=False
export GUNICORN_WORKERS=4
export GUNICORN_TIMEOUT=600
export NGINX_PROXY_READ_TIMEOUT='600s'
export NGINX_PROXY_CONNECT_TIMEOUT='600s'

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

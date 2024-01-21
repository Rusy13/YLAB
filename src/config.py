from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# DBT_HOST = os.environ.get("DBT_HOST")
# DBT_PORT = os.environ.get("DBT_PORT")
# DBT_NAME = os.environ.get("DBT_NAME")
# DBT_USER = os.environ.get("DBT_USER")
# DBT_PASS = os.environ.get("DBT_PASS")


# REDIS_HOST = os.environ.get("REDIS_HOST")
# REDIS_PORT = os.environ.get("REDIS_PORT")

# SECRET_AUTH = os.environ.get("SECRET_AUTH")
SECRET_AUTH = "my_secret_key"

# SMTP_USER = os.environ.get("SMTP_USER")
# SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
import os
from datetime import datetime
import subprocess
import time

# Configuration
NAME = "new_hmis_db"
USER = "postgres"
HOST = "localhost"
PORT = "5432"
PASSWORD = "admin"

BASE_BACKUP_DIR = r"C:\Users\paban\OneDrive\Desktop\HMIS-Backup"
PG_DUMP_PATH = r"C:\Program Files\PostgreSQL\15\bin\pg_dump"

def create_postgres_backup():
    """
    Creates a backup of the PostgreSQL database in a dynamically created folder.
    """
    # Generate current date and time strings
    current_date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    date_folder_path = os.path.join(BASE_BACKUP_DIR, current_date)
    os.makedirs(date_folder_path, exist_ok=True)

    backup_file = os.path.join(date_folder_path, f"{NAME}_backup_{timestamp}.sql")

    # Construct pg_dump command
    command = [
        PG_DUMP_PATH,
        "-h", HOST,
        "-p", PORT,
        "-U", USER,
        "-F", "p",
        "-f", backup_file,
        NAME
    ]

    try:
        # Set the PostgreSQL password environment variable
        os.environ["PGPASSWORD"] = PASSWORD

        # Execute the backup command
        subprocess.run(command, check=True, shell=True)
        print(f"Backup successful! File saved at: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed! Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Remove the password from environment variables for security
        del os.environ["PGPASSWORD"]

if __name__ == "__main__":
    while True:
        create_postgres_backup()
        time.sleep(60)

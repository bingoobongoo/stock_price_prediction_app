import subprocess

def run_comnmand(command:str):
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(process.stderr)
        raise

def run(username, database):
    backup = 'nasdaq_companies_backup.tar'

    print(f"Proceeding to create database '{database}' for user '{username}'...")
    print(f"Provide password for '{username}' if needed.")

    create_db_command = f"createdb {database} -U {username}"
    run_comnmand(create_db_command)
    print(f"Database '{database}' created successfully!\n")

    print(f"Proceeding to restore database '{database}' from {backup} for user '{username}'...")
    print(f"Provide password for '{username}' if needed.")

    restore_db_command = f"pg_restore -d {database} -U {username} {backup}"
    run_comnmand(restore_db_command)
    print(f"Database '{database}' successfully restored from '{backup}'\n")
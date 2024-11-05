import argparse
import scripts.create_db as create_db
import scripts.send_company_data as send_company_data
import scripts.download_olhc_data as download_olhc_data
import scripts.send_indicator_data as send_indicator_data
import scripts.send_financial_data as send_financial_data

def initalize_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, help='Username used to create and administrate database.')
    parser.add_argument('password', type=str, help='Password for specified user.')
    parser.add_argument('database', type=str, help='Name of database that will be created.')
    parser.add_argument('--port', type=int, default=5432, help='Port on which PostgreSQL is running.')
    return parser

parser = initalize_parser()
args = parser.parse_args()

create_db.run(args.username, args.database)
send_company_data.run(args.username, args.password, args.database, args.port)
download_olhc_data.run(args.username, args.password, args.database, args.port)
send_indicator_data.run(args.username, args.password, args.database, args.port)
send_financial_data.run(args.username, args.password, args.database, args.port)
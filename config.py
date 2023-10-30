import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--token", type=str, help="Bot token")
parser.add_argument("--db_uri", type=str, help="MongoDB URI")
parser.add_argument("--db_name", type=str, help="MongoDB database name")
parser.add_argument("--db_collection", type=str, help="MongoDB collection name")
args = parser.parse_args()


def get_token():
    if args.token:
        return args.token
    else:
        raise ValueError(
            "Bot token is missing. Please provide the token using the --token argument."
        )


def get_mongo_args():
    if args.db_uri and args.db_name and args.db_collection:
        return args.db_uri, args.db_name, args.db_collection
    else:
        raise ValueError(
            "MongoDB arguments are missing. Please provide the MongoDB URI, database name and collection name using the --db_uri, --db_name and --db_collection arguments."
        )

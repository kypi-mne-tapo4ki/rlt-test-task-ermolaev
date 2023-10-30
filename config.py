import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--token", type=str, help="Bot token")
args = parser.parse_args()


def get_token():
    if args.token:
        return args.token
    else:
        raise ValueError("Bot token is missing. Please provide the token using the --token argument.")

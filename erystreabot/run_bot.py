from ErystreaBot import ErystreaBot
from MessageResponderRegex import MessageResponderRegex
import logging
import argparse
import json
import database.DbContext as dc


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configure_path",
                        help="Path to config json", required=True)
    parser.add_argument("-s", "--connection_string",
                        help="Connection string to mongoDB", required=True)
    parser.add_argument("-d", "--database_name",
                        help="MongoDB Database name", required=True)
    args = parser.parse_args()
    with open(args.configure_path, 'r', encoding="utf-8") as f:
        config = json.load(f)

    dbContext = dc.DbContext(args.connection_string, args.database_name)
    responder = MessageResponderRegex(dbContext)
    bot = ErystreaBot(config=config, responder=responder)
    bot.launch_bot()


if __name__ == "__main__":
    main()

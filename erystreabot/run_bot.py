from ErystreaBot import ErystreaBot
from MessageResponderRegex import MessageResponderRegex
import logging
import argparse
import json

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configure_path", help="Path to config json", required=True)
    parser.add_argument("-p", "--patterns_path", help="Path to patterns json", required=True)
    args = parser.parse_args()
    with open(args.configure_path, 'r', encoding="utf-8") as f:
        config = json.load(f)
    with open(args.patterns_path, 'r', encoding="utf-8") as f:
        pattern_dict = json.load(f)
    responder = MessageResponderRegex(pattern_dict)
    bot = ErystreaBot(config=config, responder=responder)
    bot.launch_bot()

if __name__ == "__main__":
    main()
from ErystreaBot import ErystreaBot
import logging
import argparse

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configure_path", help="Path to config json", required=True)
    parser.add_argument("-p", "--patterns_path", help="Path to patterns json", required=True)
    args = parser.parse_args()
    bot = ErystreaBot(configuration_path=args.configure_path, patterns_path=args.patterns_path)
    bot.launch_bot()

if __name__ == "__main__":
    main()
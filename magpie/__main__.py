import argparse

from magpie.core import check_threshold, load_rules
from magpie.message import set_bark_token
from magpie.server import add_server_arguments, run_server


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        default="check",
        choices=["check", "server"],
        nargs="?",
        help="run http server or check threshold" "(default: %(default)s)",
    )
    parser.add_argument(
        "-r",
        "--rule",
        required=True,
        help="rules(json file)",
    )
    parser.add_argument(
        "--bark-token",
        help="bark token",
    )
    add_server_arguments(parser)
    return parser.parse_args()


def main():
    args = get_args()

    rules = load_rules(args.rule)
    set_bark_token(args.bark_token)

    if args.action == "server":
        run_server(rules)
    else:
        check_threshold(rules, send_msg_func=print)


main()

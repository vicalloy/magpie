import argparse

from magpie.core import check_threshold, load_rules, set_datasource
from magpie.message import bark_send_message, set_bark_token
from magpie.server import add_server_arguments, run_server


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        default="check",
        choices=["check", "server"],
        nargs="?",
        help="run http server or check threshold(default: %(default)s)",
    )
    parser.add_argument(
        "-r",
        "--rule",
        required=True,
        help="rules(json file)",
    )
    parser.add_argument(
        "--bark-token",
    )
    parser.add_argument(
        "-d",
        "--datasource",
        default="qq",
        choices=["qq", "tencent", "sina"],
        help="datasource(default: %(default)s)",
    )
    add_server_arguments(parser)
    return parser.parse_args()


def main():
    args = get_args()

    rules = load_rules(args.rule)
    set_bark_token(args.bark_token)
    set_datasource(args.datasource)

    if args.action == "server":
        run_server(rules)
    else:
        check_threshold(rules, send_msg_func=bark_send_message)


main()

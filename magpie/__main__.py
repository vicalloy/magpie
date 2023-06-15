import argparse

from magpie.core import check_threshold, load_rules, set_datasource
from magpie.message import (
    bark_send_message,
    set_bark_token,
    setup_telegram,
    telegram_send_message,
)
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
        "--tg-token",
        help="telegram token",
    )
    parser.add_argument(
        "--tg-chat-id",
        help="telegram chat id",
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
    set_datasource(args.datasource)

    if args.action == "server":
        run_server(rules)
    else:
        send_msg_funcs = []
        if args.bark_token:
            set_bark_token(args.bark_token)
            send_msg_funcs.append(bark_send_message)
        if args.tg_token:
            assert args.tg_chat_id, "tg-chat-id is required"
            setup_telegram(args.tg_token, int(args.tg_chat_id))
            send_msg_funcs.append(telegram_send_message)
        check_threshold(rules, send_msg_funcs=send_msg_funcs)


main()

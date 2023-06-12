import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import cast

from magpie.core import Rule, check_threshold


def html(content: str):
    return b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <pre>%s</pre>
</body>
</html>""" % content.encode(
        "utf-8"
    )


class MagpieHandler(BaseHTTPRequestHandler):
    def get_content(self) -> str:
        server = cast(MagpieServer, self.server)  # type: ignore
        return check_threshold(server.rules, send_msg_func=lambda text: text)

    def do_GET(self):  # noqa: N802
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(html(self.get_content()))
        # self.wfile.close()


class MagpieServer(HTTPServer):
    def __init__(self, *args, rules: dict[str, Rule], **kwargs):
        self.rules = rules
        super().__init__(*args, **kwargs)


def add_server_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-b",
        "--bind",
        default="0.0.0.0",
        metavar="ADDRESS",
        help="bind to this address " "(default: all interfaces)",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="bind to this port " "(default: %(default)s)",
    )


def run_server(rules: dict[str, Rule]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bind",
        default="0.0.0.0",
        metavar="ADDRESS",
        help="bind to this address " "(default: all interfaces)",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="bind to this port " "(default: %(default)s)",
    )
    args, _ = parser.parse_known_args()

    server = MagpieServer((args.bind, args.port), MagpieHandler, rules=rules)
    print(f"Started http server: {args.bind}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server({})

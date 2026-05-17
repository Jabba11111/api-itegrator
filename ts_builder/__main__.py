import argparse
import shlex
import sys

from .templates import USECASES, render


def _format_block(r):
    out = [
        f"# {r['title']}",
        f"# surface: {r['surface']}    status: {r['status']}",
        "",
        f"{r['method']} {r['url']}",
    ]
    for k, v in r["headers"].items():
        out.append(f"{k}: {v}")
    if r["body_text"] is not None and r["body_text"] != "":
        out.append("")
        out.append(r["body_text"])
    out.append("")
    out.append(f"# expected: HTTP {r['expected_status']}")
    if r["extract"]:
        out.append(f"# extract:  {r['extract']}")
    return "\n".join(out)


def _format_curl(r):
    lines = [f"curl -sS -X {r['method']}"]
    for k, v in r["headers"].items():
        lines.append(f"  -H {shlex.quote(f'{k}: {v}')}")
    if r["body_text"] is not None and r["body_text"] != "":
        lines.append(f"  --data {shlex.quote(r['body_text'])}")
    lines.append(f"  {shlex.quote(r['url'])}")
    return " \\\n".join(lines)


DEFAULT_VALUES = {
    "api_base": "https://{customer}.testersuite.nl.api.testersuite.com",
    "ui_base": "https://{customer}.testersuite.nl/{customer_id}",
    "token": "{{token}}",
    "add_action": "{{add_action — vangst nodig}}",
    "update_action": "{{update_action — vangst nodig}}",
    "remove_action": "{{remove_action — vangst nodig}}",
}


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="ts-builder",
        usage="ts-builder [--list] [--curl] <usecase> [key=value ...]",
    )
    p.add_argument("--list", action="store_true", help="list all use cases")
    p.add_argument("--curl", action="store_true", help="also print a curl command")
    p.add_argument("usecase", nargs="?", choices=sorted(USECASES.keys()),
                   help="which use case to render")
    p.add_argument("kv", nargs="*", help="key=value pairs for placeholders")
    args = p.parse_args(argv)

    if args.list or not args.usecase:
        for key, spec in USECASES.items():
            print(f"{key:24s} [{spec['surface']:6s}] {spec['status']:30s} {spec['title']}")
        return 0

    values = dict(DEFAULT_VALUES)
    for item in args.kv:
        if "=" not in item:
            print(f"bad arg (expected key=value): {item}", file=sys.stderr)
            return 2
        k, v = item.split("=", 1)
        values[k] = v

    rendered = render(args.usecase, values)
    print(_format_block(rendered))
    if args.curl:
        print()
        print("# curl:")
        print(_format_curl(rendered))
    return 0


if __name__ == "__main__":
    sys.exit(main())

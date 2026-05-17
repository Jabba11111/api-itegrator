import argparse
import json
import shlex
import sys

from .templates import USECASES, render


def _format_block(rendered):
    out = []
    out.append(f"# {rendered['title']}")
    out.append(f"# status: {rendered['status']}")
    out.append("")
    out.append(f"{rendered['method']} {rendered['url']}")
    for k, v in rendered["headers"].items():
        out.append(f"{k}: {v}")
    if rendered["body"] is not None:
        out.append("")
        out.append(json.dumps(rendered["body"], indent=2))
    out.append("")
    out.append(f"# expected: HTTP {rendered['expected_status']}")
    if rendered["extract"]:
        out.append(f"# extract:  {rendered['extract']}")
    return "\n".join(out)


def _format_curl(rendered):
    lines = [f"curl -sS -X {rendered['method']}"]
    for k, v in rendered["headers"].items():
        lines.append(f"  -H {shlex.quote(f'{k}: {v}')}")
    if rendered["body"] is not None:
        lines.append(f"  --data {shlex.quote(json.dumps(rendered['body']))}")
    lines.append(f"  {shlex.quote(rendered['url'])}")
    return " \\\n".join(lines)


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
            print(f"{key:24s} {spec['status']:8s} {spec['title']}")
        return 0

    values = {
        "base_url": "https://{customer}.testersuite.nl.api.testersuite.com",
        "token": "{{token}}",
    }
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

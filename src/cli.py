import argparse


def _handle_ingest(_: argparse.Namespace) -> None:
    print("ingest: not implemented yet")


def _handle_index(_: argparse.Namespace) -> None:
    print("index: not implemented yet")


def _handle_query(_: argparse.Namespace) -> None:
    print("query: not implemented yet")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personal RAG CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Ingest documents")
    ingest.set_defaults(func=_handle_ingest)

    index = subparsers.add_parser("index", help="Build index")
    index.set_defaults(func=_handle_index)

    query = subparsers.add_parser("query", help="Query knowledge base")
    query.set_defaults(func=_handle_query)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

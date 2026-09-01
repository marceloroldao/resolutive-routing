import json

from .router import DeterministicRouter
from .scenarios import demo_nodes, demo_request


def main() -> None:
    print(json.dumps(DeterministicRouter().route(demo_request(), demo_nodes()).as_dict(), indent=2))


if __name__ == "__main__":
    main()


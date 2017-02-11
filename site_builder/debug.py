import yaml
import json


def jprint(var: object) -> None:
    print(json.dumps(var, indent=2))


def yprint(var: object) -> None:
    print(yaml.dump(var, default_flow_style=False))

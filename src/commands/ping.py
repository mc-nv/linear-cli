import argparse

from src.client import LinearClient


def setup_parser(subparsers):
    parser = subparsers.add_parser("ping", help="Verify connection to Linear API")
    parser.set_defaults(func=execute)


def execute(args):
    try:
        client = LinearClient(token=args.token)
        print("Pinging Linear API...")
        if client.ping():
            result = client.execute_query("{ viewer { id name email } }")
            viewer = result["data"]["viewer"]
            print("✓ Connection successful!")
            print(f"  Authenticated as: {viewer['name']} ({viewer['email']})")
            print(f"  User ID: {viewer['id']}")
            return 0
        print("✗ Connection failed: Unable to reach Linear API")
        return 1
    except (ValueError, Exception) as e:
        print(f"✗ Error: {e}")
        return 1

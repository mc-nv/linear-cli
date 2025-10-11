import argparse

from src.client import LinearClient
from src.logger import get_logger


def setup_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        "ping",
        help="Verify connection to Linear API",
        parents=[parent_parser],
    )
    parser.set_defaults(func=execute)


def execute(args):
    logger = get_logger()
    
    try:
        logger.debug("Initializing ping command")
        client = LinearClient(token=args.token)
        print("Pinging Linear API...")
        if client.ping():
            result = client.execute_query("{ viewer { id name email } }")
            viewer = result["data"]["viewer"]
            logger.info(f"Connection successful - User: {viewer['name']}")
            print("✓ Connection successful!")
            print(f"  Authenticated as: {viewer['name']} ({viewer['email']})")
            print(f"  User ID: {viewer['id']}")
            return 0
        logger.warning("Connection failed")
        print("✗ Connection failed: Unable to reach Linear API")
        return 1
    except (ValueError, Exception) as e:
        logger.error(f"Ping error: {e}")
        print(f"✗ Error: {e}")
        return 1

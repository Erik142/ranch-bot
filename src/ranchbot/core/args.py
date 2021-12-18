#!/usr/bin/env python3
import argparse


def getArgsParser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="The ranch Discord bot.")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug messages",
    )
    args = parser.parse_args()
    return args

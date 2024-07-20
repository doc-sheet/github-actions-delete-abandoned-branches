from src import actions, io
import asyncio
from src.io import InputParser

if __name__ == "__main__":
    options = InputParser().parse_input()
    deleted_branches: list = asyncio.run(actions.run_action(options))
    io.format_output({"deleted_branches": deleted_branches})

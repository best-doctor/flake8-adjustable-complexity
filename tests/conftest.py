import ast
import os
from typing import List, Optional

import flake8
import pytest
from flake8.options.manager import OptionManager

from flake8_adjustable_complexity.checker import CyclomaticComplexityAdjustableChecker
from flake8_adjustable_complexity.config import Config


def get_option_manager() -> OptionManager:
    manager = OptionManager(prog='flake8', version=flake8.__version__)
    CyclomaticComplexityAdjustableChecker.add_options(manager)
    return manager


def _parse_options(manager: OptionManager, args: List[str]) -> Config:
    namespace, remaining_args = manager.parse_args(args)
    return CyclomaticComplexityAdjustableChecker.parse_options_to_config(
        manager,
        namespace,
        remaining_args,
    )


@pytest.fixture()
def parse_options():
    def with_args(args: Optional[List[str]] = None):
        return _parse_options(
            manager=get_option_manager(),
            args=args or [],
        )

    return with_args


def run_validator_for_test_file(filename, args=None):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)

    checker = CyclomaticComplexityAdjustableChecker(tree=tree, filename=filename)
    checker.config = _parse_options(
        manager=get_option_manager(),
        args=args or [],
    )

    loc_and_msg = slice(0, 3)  # exclude checker type from errors

    return [error[loc_and_msg] for error in checker.run()]

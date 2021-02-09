import ast
import os

from flake8.options.manager import OptionManager

from flake8_adjustable_complexity.checker import CyclomaticComplexityAjustableChecker


def run_validator_for_test_file(filename, args=None):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)

    if args:
        manager = OptionManager(version='1.0')
        CyclomaticComplexityAjustableChecker.add_options(manager)
        options, _ = manager.parse_args(args)
        CyclomaticComplexityAjustableChecker.parse_options(options)

    checker = CyclomaticComplexityAjustableChecker(tree=tree, filename=filename)

    return list(checker.run())

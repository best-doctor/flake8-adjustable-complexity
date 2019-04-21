import ast
import os

from flake8_adjustable_complexity.checker import CyclomaticComplexityAjustableChecker


def run_validator_for_test_file(filename):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = CyclomaticComplexityAjustableChecker(tree=tree, filename=filename)

    return list(checker.run())

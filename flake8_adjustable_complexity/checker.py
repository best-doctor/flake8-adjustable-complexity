from __future__ import annotations

import argparse
import ast
from typing import Dict, Generator, Tuple

from flake8.exceptions import ExecutionError
from flake8.options.manager import OptionManager

from flake8_adjustable_complexity import __version__ as version
from flake8_adjustable_complexity.complexity_helpers import validate_adjustable_complexity_in_tree


class CyclomaticComplexityAjustableChecker:
    BAD_VAR_NAME_PENALTY = 2
    ALLOW_SINGLE_NAMES_IN_VARS = False
    DEFAULT_MAX_MCCABE_COMPLEXITY = 7

    VAR_NAMES_BLACKLIST = {
        # from https://github.com/wemake-services/wemake-python-styleguide/
        'val',
        'vals',
        'var',
        'vars',
        'variable',
        'contents',
        'handle',
        'file',
        'objs',
        'some',
        'do',
        'no',
        'true',
        'false',
        'foo',
        'bar',
        'baz',
        'data',
        'result',
        'results',
        'item',
        'items',
        'value',
        'values',
        'content',
        'obj',
        'info',
        'handler',
    }
    SINGLE_LETTER_VAR_WHITELIST = ['_']

    name = 'flake8-adjustable-complexity'
    version = version

    _error_message_template = 'CAC001 {0} is too complex ({1} > {2})'

    max_mccabe_complexity = 0
    max_complexity_per_path: Dict[str, int] = {}

    def __init__(self, tree: ast.AST, filename: str):
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        for option in ('--max-mccabe-complexity', '--max-adjustable-complexity'):
            parser.add_option(
                option,
                type=int,
                dest='max_mccabe_complexity',
                parse_from_config=True,
                help='Max mccabe complexity',
                default=cls.DEFAULT_MAX_MCCABE_COMPLEXITY,
            )

        parser.add_option(
            '--per-path-max-adjustable-complexity',
            dest='max_complexity_per_path',
            comma_separated_list=True,
            parse_from_config=True,
            help=(
                'Comma-separated list of pairs of files or directories to '
                'check and the desired max complexity value within that path.'
            ),
            default='',
        )

    @classmethod
    def parse_options(cls, options: argparse.Namespace) -> None:
        cls.max_mccabe_complexity = int(options.max_mccabe_complexity)
        for item in options.max_complexity_per_path:
            path, max_complexity = item.split(':', maxsplit=1)
            try:
                cls.max_complexity_per_path[path] = int(max_complexity)
            except ValueError:
                raise ExecutionError(
                    "Couldn\'t parse --per-path-adjustable-max-complexity value into "
                    f'dictionary, expected number, got string "{max_complexity}"',
                )

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        max_complexity = self.max_mccabe_complexity
        if self.max_complexity_per_path:
            for path, complexity in self.max_complexity_per_path.items():
                if path in self.filename:
                    max_complexity = complexity
                    break

        too_difficult_functions = validate_adjustable_complexity_in_tree(
            self.tree,
            var_names_blacklist=self.VAR_NAMES_BLACKLIST,
            max_complexity=max_complexity,
            bad_var_name_penalty=self.BAD_VAR_NAME_PENALTY,
            allow_single_names_in_vars=self.ALLOW_SINGLE_NAMES_IN_VARS,
            single_letter_var_whitelist=self.SINGLE_LETTER_VAR_WHITELIST,
        )

        for funcdef, actual_complexity, max_expected_complexity in too_difficult_functions:
            yield (
                funcdef.lineno,
                funcdef.col_offset,
                self._error_message_template.format(funcdef.name, actual_complexity, max_expected_complexity),
                type(self),
            )

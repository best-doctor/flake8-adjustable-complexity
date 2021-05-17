from __future__ import annotations

import argparse
import ast
from typing import Generator, List, Tuple

from flake8.exceptions import ExecutionError
from flake8.options.manager import OptionManager

from flake8_adjustable_complexity import __version__ as version
from flake8_adjustable_complexity.complexity_helpers import validate_adjustable_complexity_in_tree
from flake8_adjustable_complexity.config import DEFAULT_CONFIG, Config


class CyclomaticComplexityAdjustableChecker:

    name = 'flake8-adjustable-complexity'
    version = version

    config: Config

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
                default=DEFAULT_CONFIG.max_mccabe_complexity,
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

        parser.add_option(
            '--var-names-extra-blacklist',
            dest='var_names_extra_blacklist',
            comma_separated_list=True,
            parse_from_config=True,
            help=(
                'Comma-separated list of bad variable names to blacklist. '
                'Each variable will affect the max allowed complexity.'
            ),
            default='',
        )

        parser.add_option(
            '--var-names-whitelist',
            dest='var_names_whitelist',
            comma_separated_list=True,
            parse_from_config=True,
            help=('Comma-separated list of bad variable names to whitelist. '),
            default='',
        )

    @classmethod
    def parse_options(
        cls,
        option_manager: OptionManager,
        options: argparse.Namespace,
        args: List[str],
    ) -> None:
        cls.config = cls.parse_options_to_config(option_manager, options, args)

    @classmethod
    def parse_options_to_config(
        cls,
        option_manager: OptionManager,
        options: argparse.Namespace,
        args: List[str],
    ) -> Config:
        max_complexity_per_path = {}

        for item in options.max_complexity_per_path:
            path, max_complexity = item.split(':', maxsplit=1)
            try:
                max_complexity_per_path[path] = int(max_complexity)
            except ValueError:
                raise ExecutionError(
                    "Couldn\'t parse --per-path-adjustable-max-complexity value into "
                    f'dictionary, expected number, got string "{max_complexity}"',
                )

        var_names_blacklist = DEFAULT_CONFIG.var_names_blacklist.union(
            options.var_names_extra_blacklist,
        )
        var_names_blacklist.difference_update(options.var_names_whitelist)

        return Config(
            max_mccabe_complexity=int(options.max_mccabe_complexity),
            max_complexity_per_path=max_complexity_per_path,
            var_names_blacklist=var_names_blacklist,
        )

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        max_complexity = self.config.max_mccabe_complexity
        if self.config.max_complexity_per_path:
            for path, complexity in self.config.max_complexity_per_path.items():
                if path in self.filename:
                    max_complexity = complexity
                    break

        too_difficult_functions = validate_adjustable_complexity_in_tree(
            self.tree,
            var_names_blacklist=self.config.var_names_blacklist,
            max_complexity=max_complexity,
            bad_var_name_penalty=self.config.bad_var_name_penalty,
            allow_single_names_in_vars=self.config.allow_single_names_in_vars,
            single_letter_var_whitelist=self.config.single_letter_var_whitelist,
        )

        for violation in too_difficult_functions:
            yield (
                violation.lineno,
                violation.col_offset,
                violation.message,
                type(self),
            )

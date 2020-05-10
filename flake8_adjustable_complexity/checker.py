from typing import Generator, Tuple

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

    _error_message_template = 'CAC001 is too complex ({0} > {1})'

    max_mccabe_complexity = 0

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser) -> None:
        parser.add_option(
            '--max-mccabe-complexity',
            type=int,
            parse_from_config=True,
            help='Max mccabe complexity',
            default=cls.DEFAULT_MAX_MCCABE_COMPLEXITY,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls.max_mccabe_complexity = int(options.max_mccabe_complexity)

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        too_difficult_functions = validate_adjustable_complexity_in_tree(
            self.tree,
            var_names_blacklist=self.VAR_NAMES_BLACKLIST,
            max_complexity=self.max_mccabe_complexity,
            bad_var_name_penalty=self.BAD_VAR_NAME_PENALTY,
            allow_single_names_in_vars=self.ALLOW_SINGLE_NAMES_IN_VARS,
            single_letter_var_whitelist=self.SINGLE_LETTER_VAR_WHITELIST,
        )

        for funcdef, actual_complexity, max_expected_complexity in too_difficult_functions:
            yield (
                funcdef.lineno,
                funcdef.col_offset,
                self._error_message_template.format(actual_complexity, max_expected_complexity),
                type(self),
            )

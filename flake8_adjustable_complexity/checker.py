from typing import Generator, Tuple

from flake8_adjustable_complexity import __version__ as version
from flake8_adjustable_complexity.complexity_helpers import validate_adjustable_complexity_in_tree


class CyclomaticComplexityAjustableChecker:
    name = 'flake8-adjustable-complexity'
    version = version

    _error_message_template = 'CCE001 is too complex ({0} > {1})'

    DEFAULT_MAX_MCCABE_COMPLEXITY = 7
    BAD_VAR_NAME_PENALTY = 2
    ALLOW_SINGLE_NAMES_IN_VARS = False

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

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        too_difficult_functions = validate_adjustable_complexity_in_tree(
            self.tree,
            var_names_blacklist=self.VAR_NAMES_BLACKLIST,
            default_max_complexity=self.DEFAULT_MAX_MCCABE_COMPLEXITY,
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

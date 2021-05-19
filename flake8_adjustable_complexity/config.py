from typing import Dict, List, NamedTuple, Set

BAD_VAR_NAME_PENALTY: int = 2
ALLOW_SINGLE_NAMES_IN_VARS: bool = False
DEFAULT_MAX_MCCABE_COMPLEXITY: int = 7

DEFAULT_VAR_NAMES_BLACKLIST: Set[str] = {
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
SINGLE_LETTER_VAR_WHITELIST: List[str] = ['_']


class Config(NamedTuple):
    max_mccabe_complexity: int
    max_complexity_per_path: Dict[str, int]
    var_names_blacklist: Set[str]
    bad_var_name_penalty: int = BAD_VAR_NAME_PENALTY
    allow_single_names_in_vars: bool = ALLOW_SINGLE_NAMES_IN_VARS
    single_letter_var_whitelist: List[str] = SINGLE_LETTER_VAR_WHITELIST


DEFAULT_CONFIG = Config(
    max_mccabe_complexity=DEFAULT_MAX_MCCABE_COMPLEXITY,
    max_complexity_per_path={},
    var_names_blacklist=DEFAULT_VAR_NAMES_BLACKLIST,
)

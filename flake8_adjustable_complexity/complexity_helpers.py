import ast
from typing import Optional, List, Tuple, Set

import mccabe

from flake8_adjustable_complexity.ast_helpers import get_all_funcdefs_from, \
    extract_all_vars_in_node


def validate_adjustable_complexity_in_tree(
    tree: ast.AST,
    var_names_blacklist: Set[str],
    default_max_complexity: int,
    bad_var_name_penalty: int,
    allow_single_names_in_vars: bool,
    single_letter_var_whitelist: Optional[List[str]] = None,
) -> List[Tuple[ast.AST, int, int]]:
    errors = []
    for funcdef in get_all_funcdefs_from(tree):
        error_in_funcdef = check_funcdef_adjustable_complexity(
            funcdef,
            var_names_blacklist,
            default_max_complexity,
            bad_var_name_penalty,
            allow_single_names_in_vars,
            single_letter_var_whitelist,
        )
        if error_in_funcdef:
            errors.append(error_in_funcdef)
    return errors


def check_funcdef_adjustable_complexity(
    funcdef: ast.FunctionDef,
    var_names_blacklist: Set[str],
    default_max_complexity: int,
    bad_var_name_penalty: int,
    allow_single_names_in_vars: bool,
    single_letter_var_whitelist: Optional[List[str]] = None,
) -> Optional[Tuple[ast.AST, int, int]]:
    single_letter_var_whitelist = single_letter_var_whitelist or []
    funcdef_vars = extract_all_vars_in_node(funcdef)
    vars_from_blacklist_amount = sum(1 for v in funcdef_vars if v in var_names_blacklist)
    additional_penalty = 0
    if not allow_single_names_in_vars:
        additional_penalty = (
            sum(1 for v in funcdef_vars if len(v) == 1 and v not in single_letter_var_whitelist)
            * vars_from_blacklist_amount
        )
    max_allowed_cyclomatic_complexity = (
        default_max_complexity
        - bad_var_name_penalty
        * vars_from_blacklist_amount
        - additional_penalty
    )
    current_mccabe_complexity = get_mccabe_complexity_for(funcdef)
    if current_mccabe_complexity > max_allowed_cyclomatic_complexity:
        return funcdef, current_mccabe_complexity, max_allowed_cyclomatic_complexity


def get_mccabe_complexity_for(node: ast.AST) -> int:
    visitor = mccabe.PathGraphingAstVisitor()
    visitor.preorder(node, visitor)
    return list(visitor.graphs.values())[0].complexity()

import ast
from typing import List, Optional, Set

import mccabe

from flake8_adjustable_complexity.ast_helpers import (
    FuncDef,
    extract_all_vars_in_node,
    get_all_funcdefs_from,
)
from flake8_adjustable_complexity.violations import ComplexityViolation, PenaltyTooHighViolation


def validate_adjustable_complexity_in_tree(
    tree: ast.AST,
    var_names_blacklist: Set[str],
    max_complexity: int,
    bad_var_name_penalty: int,
    allow_single_names_in_vars: bool,
    single_letter_var_whitelist: Optional[List[str]] = None,
) -> List[ComplexityViolation]:
    violations = []
    for funcdef in get_all_funcdefs_from(tree):
        violation_in_funcdef = check_funcdef_adjustable_complexity(
            funcdef,
            var_names_blacklist,
            max_complexity,
            bad_var_name_penalty,
            allow_single_names_in_vars,
            single_letter_var_whitelist,
        )
        if violation_in_funcdef:
            violations.append(violation_in_funcdef)
    return violations


def check_funcdef_adjustable_complexity(
    funcdef: FuncDef,
    var_names_blacklist: Set[str],
    default_max_complexity: int,
    bad_var_name_penalty: int,
    allow_single_names_in_vars: bool,
    single_letter_var_whitelist: Optional[List[str]] = None,
) -> Optional[ComplexityViolation]:
    single_letter_var_whitelist = single_letter_var_whitelist or []
    funcdef_vars = extract_all_vars_in_node(funcdef)
    vars_from_blacklist_amount = sum(1 for v in funcdef_vars if v in var_names_blacklist)
    additional_penalty = 0
    if not allow_single_names_in_vars:
        additional_penalty = (
            sum(1 for v in funcdef_vars if len(v) == 1 and v not in single_letter_var_whitelist)
            * vars_from_blacklist_amount
        )
    penalty = bad_var_name_penalty * vars_from_blacklist_amount + additional_penalty
    max_allowed_cyclomatic_complexity = default_max_complexity - penalty

    current_mccabe_complexity = get_mccabe_complexity_for(funcdef)
    if current_mccabe_complexity > max_allowed_cyclomatic_complexity:
        lineno = funcdef.lineno
        col_offset = funcdef.col_offset

        context = {
            'funcdef': funcdef,
            'current_mccabe_complexity': current_mccabe_complexity,
            'max_allowed_cyclomatic_complexity': max_allowed_cyclomatic_complexity,
            'default_max_complexity': default_max_complexity,
            'penalty': penalty,
        }
        if max_allowed_cyclomatic_complexity > 0:
            return ComplexityViolation(lineno, col_offset, **context)
        else:
            return PenaltyTooHighViolation(lineno, col_offset, **context)


def get_mccabe_complexity_for(node: ast.AST) -> int:
    visitor = mccabe.PathGraphingAstVisitor()
    visitor.preorder(node, visitor)
    return list(visitor.graphs.values())[0].complexity()

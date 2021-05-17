import ast
from typing import List, Union

from flake8_adjustable_complexity.list_helpers import flat

FuncDef = Union[ast.FunctionDef, ast.AsyncFunctionDef]


def get_all_funcdefs_from(tree: ast.AST) -> List[FuncDef]:
    return [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def extract_all_vars_in_node(ast_tree: ast.AST) -> List[str]:
    var_info: List[str] = []
    assignments = [n for n in ast.walk(ast_tree) if isinstance(n, ast.Assign)]
    var_info += flat([get_var_names_from_assignment(a) for a in assignments])
    ann_assignments = [n for n in ast.walk(ast_tree) if isinstance(n, ast.AnnAssign)]
    var_info += flat([get_var_names_from_assignment(a) for a in ann_assignments])
    funcdefs = [n for n in ast.walk(ast_tree) if isinstance(n, ast.FunctionDef)]
    var_info += flat([get_var_names_from_funcdef(f) for f in funcdefs])
    fors = [n for n in ast.walk(ast_tree) if isinstance(n, ast.For)]
    var_info += flat([get_var_names_from_for(f) for f in fors])
    return var_info


def get_var_names_from_assignment(
    assignment_node: Union[ast.Assign, ast.AnnAssign],
) -> List[str]:
    if isinstance(assignment_node, ast.AnnAssign):
        if isinstance(assignment_node.target, ast.Name):
            return [assignment_node.target.id]
    elif isinstance(assignment_node, ast.Assign):
        names = [t for t in assignment_node.targets if isinstance(t, ast.Name)]
        return [n.id for n in names]
    return []


def get_var_names_from_funcdef(funcdef_node: ast.FunctionDef) -> List[str]:
    vars_info = []
    for arg in funcdef_node.args.args:
        vars_info.append(arg.arg)
    return vars_info


def get_var_names_from_for(for_node: ast.For) -> List[str]:
    if isinstance(for_node.target, ast.Name):
        return [for_node.target.id]
    elif isinstance(for_node.target, ast.Tuple):
        return [n.id for n in for_node.target.elts if isinstance(n, ast.Name)]
    return []

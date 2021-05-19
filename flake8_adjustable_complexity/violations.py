from typing import Any, Dict


GenericContext = Dict[str, Any]


class BaseViolation:
    code: str
    error_template: str
    lineno: int
    col_offset: int

    def __init__(self, lineno: int, col_offset: int, **context: Any) -> None:
        self.lineno = lineno
        self.col_offset = col_offset
        self.message = self.format_message(**self.get_context(**context))

    @classmethod
    def format_message(cls, **context: Any) -> str:
        error = cls.error_template.format(**context)
        return f'{cls.code} {error}'

    def get_context(self, **context: Any) -> GenericContext:
        return context


class ComplexityViolation(BaseViolation):
    code = 'CAC001'
    error_template = '{func} is too complex ({complexity} > {max_complexity})'

    def get_context(self, **context: Any) -> GenericContext:
        return {
            'func': context['funcdef'].name,
            'complexity': context['current_mccabe_complexity'],
            'max_complexity': context['max_allowed_cyclomatic_complexity'],
        }


class PenaltyTooHighViolation(ComplexityViolation):
    code = 'CAC002'
    error_template = (
        '{func} is too complex ({complexity}). '
        'Bad variable names penalty is too high ({penalty})'
    )

    def get_context(self, **context: Any) -> GenericContext:
        return {
            'func': context['funcdef'].name,
            'complexity': context['current_mccabe_complexity'],
            'penalty': context['penalty'],
        }

import pytest
from conftest import run_validator_for_test_file

from flake8_adjustable_complexity.violations import ComplexityViolation, PenaltyTooHighViolation


@pytest.mark.parametrize(
    ('filename', 'args', 'expected'),
    [
        (
            'code_CAC001.py',
            None,
            {
                (
                    1,
                    0,
                    ComplexityViolation.format_message(
                        func='foo',
                        complexity=10,
                        max_complexity=7,
                    ),
                ),
            },
        ),
        (
            'code_CAC002.py',
            None,
            {
                (
                    1,
                    0,
                    PenaltyTooHighViolation.format_message(
                        func='foo',
                        complexity=10,
                        penalty=10,
                    ),
                ),
            },
        ),
        (
            'too_complex_with_blacklisted.py',
            [
                '--per-path-max-adjustable-complexity',
                'too_complex_with_blacklisted.py:99',
            ],
            set(),
        ),
        (
            'too_complex_with_blacklisted.py',
            [
                '--var-names-whitelist=vars,info,obj',
            ],
            set(),
        ),
        (
            'too_complex_with_blacklisted.py',
            [
                '--var-names-whitelist=vars,info ',
                '--max-adjustable-complexity=1',
            ],
            {
                (
                    1,
                    0,
                    PenaltyTooHighViolation.format_message(
                        func='foo',
                        complexity=4,
                        penalty=2,
                    ),
                ),
            },
        ),
    ],
)
def test_checker(filename, args, expected):
    errors = run_validator_for_test_file(filename, args)

    assert set(errors) == expected

from conftest import run_validator_for_test_file


def test_get_error_for_too_complex_file():
    errors = run_validator_for_test_file('too_complex.py')
    assert len(errors) == 1


def test_get_error_for_not_too_complex_file_with_blacklisted_vars():
    errors = run_validator_for_test_file('too_complex_with_blacklisted.py')
    assert len(errors) == 1


def test_get_no_error_for_per_path_excluded_file():
    errors = run_validator_for_test_file(
        'too_complex_with_blacklisted.py',
        args=[
            '--per-path-max-adjustable-complexity',
            'too_complex_with_blacklisted.py:99',
        ],
    )
    assert len(errors) == 0


def test_get_error_for_per_path_not_excluded_file():
    errors = run_validator_for_test_file(
        'too_complex.py',
        args=[
            '--per-path-max-adjustable-complexity',
            'too_complex_with_blacklisted.py:99',
        ],
    )
    assert len(errors) == 1

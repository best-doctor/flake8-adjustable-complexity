from conftest import run_validator_for_test_file


def test_get_error_for_too_complex_file():
    errors = run_validator_for_test_file('too_complex.py')
    assert len(errors) == 1


def test_get_error_for_not_too_complex_file_with_blacklisted_vars():
    errors = run_validator_for_test_file('too_complex_with_blacklisted.py')
    assert len(errors) == 1

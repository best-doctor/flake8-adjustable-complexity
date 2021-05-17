import pytest
from flake8.exceptions import ExecutionError

from flake8_adjustable_complexity.config import DEFAULT_CONFIG


@pytest.mark.parametrize(
    ('args', 'max_mccabe_complexity'),
    [
        (['--max-mccabe-complexity=5'], 5),
        (['--max-adjustable-complexity=10'], 10),
        ([], DEFAULT_CONFIG.max_mccabe_complexity),
    ],
)
def test_parse_max_mccabe_complexity(parse_options, args, max_mccabe_complexity):
    config = parse_options(args)

    assert config.max_mccabe_complexity == max_mccabe_complexity


@pytest.mark.parametrize(
    ('args', 'max_complexity_per_path'),
    [
        (
            [
                '--per-path-max-adjustable-complexity',
                'foo.py:10,bar.py:20',
            ],
            {
                'foo.py': 10,
                'bar.py': 20,
            },
        ),
        ([], DEFAULT_CONFIG.max_complexity_per_path),
    ],
)
def test_parse_max_complexity_per_path(parse_options, args, max_complexity_per_path):
    config = parse_options(args)

    assert config.max_complexity_per_path == max_complexity_per_path


def test_parse_max_complexity_per_path_error(parse_options):
    args = [
        '--per-path-max-adjustable-complexity',
        'foo.py:invalid-complexity',
    ]

    with pytest.raises(ExecutionError) as excinfo:
        parse_options(args)

    assert "Couldn\'t parse --per-path-adjustable-max-complexity" in str(excinfo.value)


@pytest.mark.parametrize(
    ('args', 'var_names_blacklist'),
    [
        (
            ['--var-names-extra-blacklist=my_obj,my_var'],
            DEFAULT_CONFIG.var_names_blacklist | {'my_obj', 'my_var'},
        ),
        (
            ['--var-names-whitelist=var,result'],
            DEFAULT_CONFIG.var_names_blacklist - {'var', 'result'},
        ),
        (
            [
                '--var-names-extra-blacklist=my_obj,my_var',
                '--var-names-whitelist=var,result',
            ],
            (DEFAULT_CONFIG.var_names_blacklist | {'my_obj', 'my_var'}) - {'var', 'result'},
        ),
        ([], DEFAULT_CONFIG.var_names_blacklist),
    ],
)
def test_parse_var_names_blacklist(parse_options, args, var_names_blacklist):
    config = parse_options(args)

    assert config.var_names_blacklist == var_names_blacklist

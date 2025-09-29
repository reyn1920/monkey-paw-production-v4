from unittest import mock

from pkg_resources import evaluate_marker


@mock.patch('platform.python_version', return_value='2710')
def test_ordering(python_version_mock):
    assert evaluate_marker("python_full_version > '273'") is True
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "spark: tests that require local PySpark")


@pytest.mark.spark
def test_spark_dummy():
    assert 1 + 1 == 2

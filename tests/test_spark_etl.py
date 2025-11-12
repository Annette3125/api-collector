import os
import pytest

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")

def test_spark_module_imports():
    """Quick smoke test: is pyspark present, is the ETL module importing."""
    try:
        import pyspark  # noqa:F401
    except Exception:
        pytest.skip("pyspark is not installed in CI or locally - skipping Spark test")

    # if spark exist – check, our model is imported
    from api_collector import databricks_etl  # noqa:F401

def test_latest_csv_exists_or_skip():
    """if exist `data/new/stock_data_latest.csv` - validate it; if not, skip it."""
    latest = os.path.join("data", "new", "stock_data_latest.csv")
    if not os.path.exists(latest):
        pytest.skip("no latest CSV generated - run get_data.py or skip the test")
    # minimal check
    with open(latest, "r", encoding="utf-8") as f:
        head = f.readline()
    assert "date" in head and "symbol" in head
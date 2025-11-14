# API Collector — ETL Pipeline (Python → CSV/Parquet → S3 → Spark)

A small end-to-end ETL-style data pipeline demonstrating real-world data engineering:
	•	Extract stock data from the Alpha Vantage API
	•	Transform with Pandas (cleaning, validation, typing)
	•	Load locally into CSV + Parquet
	•	Optionally upload to AWS S3
	•	Process with PySpark (local Databricks-style ETL)
	•	Run tests via GitHub Actions CI
---

 This project demonstrates how Python, CI, AWS, and Spark can work together in a small, clear, end-to-end data pipeline.


## 🧩 Features

### Extract
    • Pulls TIME_SERIES_DAILY stock data via Alpha Vantage API
    • Supports multiple symbols (configurable in `.env`)
    • Handles rate limits and HTTP errors

### Transform
	•	Renames and normalizes columns
	•	Converts datatypes (numeric, datetime)
	•	Drops invalid rows (negative or missing prices)
	•	Sorts by date

### Load
Load
	•	Saves fresh snapshot as:
	•	data/new/stock_data_latest.csv
	•	timestamped history files
	•	Parquet outputs for further analytics


 Upload to AWS S3
	•	Uses boto3
	•	Stores processed CSV into S3 bucket:
s3://annette-etl-data/raw/stock_data_latest.csv

Spark ETL (local)
	•	Reads CSV with PySpark
	•	Computes average daily price
	•	Aggregates mean price per symbol
	•	Saves Parquet to data/processed/

---

## 🛠️ Technologies

- **Python 3.11+**
- **Requests** – API integration  
- **Pandas** – data transformation  
- **python-dotenv** – environment management  
- **Schedule / Logging** – automation & monitoring  
- **Pytest** – unit testing  
- **GitHub Actions CI** 
- **(S3 + IAM + CLI)**
- 
---

## ⚙️ Setup

## Prerequisites

Before you start, make sure you have:

- **Python 3.11+** installed  
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

##  Clone
```bash
git clone https://github.com/Annette3125/api-collector.git
cd api-collector
```

### Installation

 Code Editor
- A code editor or IDE of your choice 
- Recommended  PyCharm Community Edition or VS Code 
- Any editor that supports Python will work.

---
### Virtual environment
- For Linux/Mac
```
python3 -m venv venv
```

- For Windows 

```
python -m venv venv
```

### Activate the virtual environment

- For Linux/Mac:

```bash 
source venv/bin/activate
```

- For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

- For Windows CMD:

```bash
.venv\Scripts\activate.bat
```

## Upgrade pip (all OS)
```bash
python -m pip install --upgrade pip
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

🔑  Environment Variables

Set environment variables:
Create .env file in the project's root directory and add environment variable to this file.
Example '.env' file:

```                   
ALPHA_VANTAGE_API_KEY=<your-api-key>
SYMBOLS=AAPL,GOOGL,MSFT
DATA_DIR=data/new
RATE_LIMIT_SLEEP=15

```

You can get a free API key from [Alpha Vantage](https://youtu.be/uqUoILc_1NY?si=BGdpGAePwqGA4pTL)￼.

▶️ Run Extract + Transform + Load


```bash
python -m api_collector.get_data

```

Outputs:
      •	data/new/stock_data_latest.csv 
      •	timestamped CSV + Parquet history

Run the daily schedular:

```bash
python -m api_collector.scheduler
```
Saves data/new/stock_data.csv with columns: date, open, high
CSV file will be generated in directory data/new/.

Example of csv output:

```
data,open,high,low,close,volume,symbol
2025-11-04,511.76,515.55,507.84,514.33,20958663,MSFT
2025-11-05,513.3,514.83,506.575,507.16,22883851,MSFT
2025-11-06,505.66,505.7,495.81,497.1,27406496,MSFT
2025-11-07,496.945,499.377,493.25,496.82,24019764,MSFT
2025-11-10,500.035,506.85,498.8,506.0,26045011,MSFT
```


☁️ AWS S3 Integration

Configure AWS CLI
```bash
aws configure
```
You need:
	•	Access Key
	•	Secret Key
	•	Region (eu-north-1)


Upload latest CSV to S3
```bash
python -m api_collector.upload_to_s3
```

File appears at:
```bash
s3://annette-etle-data/raw/stock_data_latest.csv

```

🔥 Local Spark ETL (Databricks-style)

macOS prerequisites
```bash
export JAVA_HOME="$(/usr/libexec/java_home -v 17)"
export SPARK_LOCAL_IP=127.0.0.1
```


Run ETL 

```bash
python -m api_collector.databricks_etl
```
or via script:

```bash
./scripts/run_spark.sh
```

data/processed/stock_summary.parquet


🧪 Testing

```bash
pytest -q
```
CI runs automatically on every GitHub push.



Alternatively, you can run the ETL directly using:
```bash
./scripts/run_spark.sh
```

🚀 Future Improvements

- Upload processed Parquet to AWS S3
- Add Athena table definitions (run SQL on S3 data)
- Build Airflow or Prefect DAG for scheduling
- Add SQLite or Django ORM for persistent storage
- Add dashboards (Streamlit)
- Deploy a small FastAPI service to AWS
 
✨ Author

Created by Annette 💙

Demonstrating data extraction, cleaning, transformation, 
and loading using public financial APIs.





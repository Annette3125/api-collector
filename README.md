# API-collector

A small **ETL-style data pipeline** project that demonstrates data extraction, transformation, and loading using the **Alpha Vantage API**.

The script collects daily stock data for several symbols, cleans and validates it, and saves both CSV and Parquet snapshots for further analysis.

---

## 🧩 Features

### Extract
- Fetches stock data from Alpha Vantage API (`TIME_SERIES_DAILY`)
- Supports multiple symbols (configurable in `.env`)
- Handles rate limits and API errors

### Transform
- Cleans and renames columns  
- Converts types to numeric and datetime  
- Removes duplicates and invalid values  
- Sorts data in ascending date order

### Load
- Saves results to CSV and (optionally) Parquet  
- Keeps a timestamped history and updates `stock_data_latest.csv`

---

## 🛠️ Technologies

- **Python 3.11+**
- **Requests** – API integration  
- **Pandas** – data transformation  
- **python-dotenv** – environment management  
- **Schedule / Logging** – automation & monitoring  
- **Pytest** – unit testing  

---

## ⚙️ Setup

## Prerequisites

Before you start, make sure you have:

- **Python 3.11+** installed  
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)


### Installation Steps

### Code Editor

- A code editor or IDE of your choice
- Recommended  PyCharm Community Edition or VS Code
- Any editor that supports Python will work.


## Installation

---
### Create virtual environment in project's root directory:
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

## Dependencies

```bash
pip install -r requirements.txt
```

## Clone the Repo

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## Development
 - I use **Black** and **Isort** for code styling and formatting.

```bash
pip install black isort
```


🔑  Configuration
#### Set environment variables:

Create .env file in the project's root directory and add environment variable to this file.

Example '.env' file:

```                   
ALPHA_VANTAGE_API_KEY=<your-api-key>
SYMBOLS=AAPL,GOOGL,MSFT
DATA_DIR=data/new
RATE_LIMIT_SLEEP=15

```

You can get a free API key from [Alpha Vantage](https://youtu.be/uqUoILc_1NY?si=BGdpGAePwqGA4pTL)￼.

▶️ Usage and Running

#### How to run script:

```bash
python get_data.py

```

Run the daily schedular:

```bash
python scheduler.py
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

#### How to run scheduler:

```bash
python scheduler.py
```

🧪 Testing

```bash
pytest -q
```
Sample test file:
tests/test_transform.py checks:

 -- column naming and data types
 -- ascending order bu date
 -- filtering invalid values

#### Run local PySpark ETL


### Mini Spark ETL (local Databricks-style)

- Reads `data/new/stock_data_latest.csv` with PySpark
- Cleans invalid prices, computes daily `avg_price`
- Aggregates mean price per `symbol`
- Saves Parquet to `data/processed/stock_summary.parquet`



- Make sure Java 17 is installed.
- On macOS:
```bash
  export JAVA_HOME="$(/usr/libexec/java_home -v 17)"
  export SPARK_LOCAL_IP=127.0.0.1
```

Alternatively, you can run the ETL directly using:
```bash
./scripts/run_spark.sh
```

 -- Activate venv and run:
python -m api_collector.databricks_etl

Future Improvements

 - - Add SQLite or Django ORM integration for persistent storage.
 - - Visualize data using Matplotlib or Chart.js
 - - Deploy automated testing with GitHub Actions CI
 

Created by Annette

Demonstrating data extraction, cleaning, transformation, 
and loading using public financial APIs.





# Api-collector

API Data Collector: fetches, processes & saves via Alpha Vantage API 
(Python, requests, pandas, CSV output, dotenv, schedule).


## Prerequisites

Before you start, make sure you have:

- **Python 3.11+** installed  
  Download from https://www.python.org/downloads/  
- **Git** installed (for cloning the repo) 

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

```commandline 
source venv/bin/activate
```

- For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

- For Windows CMD:

```comandline
.venv\Scripts\activate.bat
```

## Upgrade pip (all OS)
```commandline
python -m pip install --upgrade pip
```

## Dependencies

```commandline
pip install -r requirements.txt
```

## Clone the Repo

```commandline
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## Development
 - I use **Black** and **Isort** for code styling and formatting.

```commandline
pip install black isort
```


## Usage and Running

#### Set environment variables:

Create .env file in the project's root directory and add environment variable to this file.

Example '.env' file:

```                   
ALPHA_VANTAGE_API_KEY=<ATTUYE7TR1MNPO1R>

```


#### How to run script:

```commandline
python get_data.py

```
CSV file will be generated in directory data/new/.

There is example of csv output:

,open,high,low,close,volume,symbol
2025-05-30,199.37,201.96,196.78,200.85,70819942.0,AAPL

2025-05-29,203.575,203.81,198.51,199.95,51477938.0,AAPL

2025-05-20,166.43,168.5,162.9,163.98,46607656.0,GOOGL

2025-05-19,164.51,166.64,164.22,166.54,30426097.0,GOOGL

2025-04-10,382.06,383.9,367.8,381.35,38024368.0,MSFT

2025-04-09,353.535,393.225,353.1,390.49,50199696.0,MSFT




#### How to run scheduler:

```commandline
python scheduler.py
```

Time - tz=Europe/Vilnius


### Api references

 - URL: https://www.alphavantage.co/

 - Method: GET

   - Parameters:
 
      - - "function": "TIME_SERIES_DAILY", required: function,
   The time series of your choice. In this case, function=TIME_SERIES_DAILY

   
      - - "symbol": symbol, 
required: symbol, required: symbol,
The name of the equity of your choice. For example: symbol=IBM
      
      - - "outputsize": "compact",
optional

      - - "apikey": API_KEY, 
required: "apikey"
Your API key.
Claim your free API key [Alpha Vantage](https://www.alphavantage.co/support/#api-key)




A quick note at the end you can deactivate, to avoid 
accidentally installing packages into wrong
environment:
```commandline
deactivate
```
And activate as you start again.





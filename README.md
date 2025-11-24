# Average Daily Balance Calculator

A Python tool to calculate the average daily balance from bank statement data. This is useful for determining monthly average balances required by banks for maintaining account benefits or meeting minimum balance requirements.

## Features

- Calculate average daily balance from CSV transaction data
- Automatically carries forward previous balance for missing days
- Supports custom date ranges or auto-detects from data
- Provides detailed calculation breakdown
- Handles multiple transactions per day (uses end-of-day balance)
- Interactive user input for CSV file selection

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository:
```bash
cd adbcalculator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Alternatively, install pandas directly:
```bash
pip install pandas
```

## CSV Format

The program expects a CSV file with **no header** and **two columns**:

1. **DATE** - Transaction date in YYYY-MM-DD format
2. **ENDING BALANCE** - The account balance (numeric value)

### Example CSV Format

```csv
2024-01-01,15000.00
2024-01-02,14500.50
2024-01-03,16200.75
2024-01-05,13800.00
2024-01-08,12500.25
2024-01-10,18900.00
2024-01-15,17300.50
2024-01-20,16800.00
2024-01-25,15500.75
2024-01-31,14200.00
```

**Note:** 
- Dates don't need to be consecutive - missing days will carry forward the previous day's balance
- Multiple entries for the same day are allowed - the last entry will be used as the end-of-day balance
- No header row should be present in the CSV file

## Usage

### Basic Usage

1. Create your CSV file with your transaction data (see format above)

2. Run the calculator:
```bash
python main.py
```

3. When prompted, enter the name of your CSV file:
```
Enter the CSV file name (e.g., sample.csv): your_data.csv
```

### Advanced Usage

You can also use the function programmatically with custom date ranges:

```python
from main import calculate_average_daily_balance

# Auto-detect date range from data
results = calculate_average_daily_balance('sample.csv')

# Or specify custom date range
results = calculate_average_daily_balance(
    'sample.csv',
    month_start='2024-01-01',
    month_end='2024-01-31'
)

print(f"Average Daily Balance: PHP {results['average_daily_balance']:,.2f}")
```

## Output Example

```
==================================================
AVERAGE DAILY BALANCE CALCULATION
==================================================
Period: 2024-01-01 to 2024-01-31
Total days in period: 31
Days with transactions: 10
Days with zero balance: 21

First transaction: 2024-01-01
Last transaction: 2024-01-31

Starting balance: PHP 15,000.00
Ending balance: PHP 14,200.00

Sum of all daily balances: PHP 159,700.75
Average Daily Balance: PHP 5,151.64
==================================================
```

## How It Works

The average daily balance is calculated using the formula:

**Average Daily Balance = Sum of all daily balances / Total days in period**

The calculator:
1. Reads your transaction data from the CSV file
2. Sorts transactions chronologically
3. For each date with multiple transactions, uses the last (end-of-day) balance
4. Creates a complete date range for the calculation period
5. Fills missing dates by carrying forward the previous day's balance
6. Sums all daily balances
7. Divides by the total number of days in the period

## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome!

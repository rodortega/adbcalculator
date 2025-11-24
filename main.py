import pandas as pd

def calculate_average_daily_balance(csv_file_path, month_start=None, month_end=None):
    """
    Calculate the average daily balance from a CSV file containing daily bank balances.
    
    Formula: Sum of all daily balances / Total days in period
    
    Args:
        csv_file_path (str): Path to the CSV file with DATE and ENDING BALANCE columns
        month_start (str): Optional start date (YYYY-MM-DD). If not provided, uses first day of month from data
        month_end (str): Optional end date (YYYY-MM-DD). If not provided, uses last day of month from data
    
    Returns:
        dict: Contains calculation details and results
    """
    
    # Read the CSV file (no header, two columns: date and balance)
    df = pd.read_csv(csv_file_path, header=None, names=['DATE', 'ENDING BALANCE'])
    
    # Convert DATE column to datetime
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    # Sort by date to ensure chronological order
    df = df.sort_values('DATE')
    
    # Group by date and take the last balance of each day (end of day balance)
    daily_balances = df.groupby('DATE')['ENDING BALANCE'].last().reset_index()
    
    # Determine the calculation period
    if month_start:
        start_date = pd.to_datetime(month_start)
    else:
        # Use the first day of the month from the earliest date in data
        first_date = daily_balances['DATE'].min()
        start_date = first_date.replace(day=1)
    
    if month_end:
        end_date = pd.to_datetime(month_end)
    else:
        # Use the last day of the month from the latest date in data
        last_date = daily_balances['DATE'].max()
        # Get last day of month
        if last_date.month == 12:
            end_date = last_date.replace(day=31)
        else:
            end_date = (last_date.replace(day=1, month=last_date.month + 1) - pd.Timedelta(days=1))
    
    # Create a complete date range for the period
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create a dataframe with all dates in the period
    all_dates = pd.DataFrame({'DATE': date_range})
    
    # Merge with actual balances, filling missing dates with 0 balance
    complete_balances = all_dates.merge(daily_balances, on='DATE', how='left')
    complete_balances['ENDING BALANCE'] = complete_balances['ENDING BALANCE'].fillna(0)
    
    # Calculate total days in the period
    total_days = len(complete_balances)
    
    # Sum all daily balances (including days with 0 balance)
    total_balance_sum = complete_balances['ENDING BALANCE'].sum()
    
    # Calculate average daily balance: Sum of all daily balances / Total days
    average_daily_balance = total_balance_sum / total_days
    
    # Create results dictionary
    results = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'actual_days_with_data': len(daily_balances),
        'total_days_in_period': total_days,
        'days_with_zero_balance': total_days - len(daily_balances),
        'first_transaction_date': daily_balances['DATE'].min().strftime('%Y-%m-%d'),
        'last_transaction_date': daily_balances['DATE'].max().strftime('%Y-%m-%d'),
        'starting_balance': daily_balances['ENDING BALANCE'].iloc[0],
        'ending_balance': daily_balances['ENDING BALANCE'].iloc[-1],
        'total_balance_sum': total_balance_sum,
        'average_daily_balance': average_daily_balance,
        'daily_balances': daily_balances,
        'complete_balances': complete_balances
    }
    
    return results

def main():
    # Example usage - replace with your CSV file path
    csv_file_path = 'sample.csv'
    
    try:
        results = calculate_average_daily_balance(csv_file_path)
        
        print("=" * 50)
        print("AVERAGE DAILY BALANCE CALCULATION")
        print("=" * 50)
        print(f"Period: {results['start_date']} to {results['end_date']}")
        print(f"Total days in period: {results['total_days_in_period']}")
        print(f"Days with transactions: {results['actual_days_with_data']}")
        print(f"Days with zero balance: {results['days_with_zero_balance']}")
        print(f"\nFirst transaction: {results['first_transaction_date']}")
        print(f"Last transaction: {results['last_transaction_date']}")
        print(f"\nStarting balance: PHP {results['starting_balance']:,.2f}")
        print(f"Ending balance: PHP {results['ending_balance']:,.2f}")
        print(f"\nSum of all daily balances: PHP {results['total_balance_sum']:,.2f}")
        print(f"Average Daily Balance: PHP {results['average_daily_balance']:,.2f}")
        print("=" * 50)
        
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file '{csv_file_path}'")
        print("Please make sure the file exists and the path is correct.")
    except Exception as e:
        print(f"Error processing the data: {str(e)}")

if __name__ == "__main__":
    main()
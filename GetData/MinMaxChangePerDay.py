import json
from collections import Counter, defaultdict

with open('solana.json', 'r', encoding='utf8') as f:
    data = json.load(f)

# Helper functions

def group_by(grouper, rows, value_transform=None):
    '''key is output of grouper, value is list of rows'''
    grouped = defaultdict(list)
    for row in rows:
        grouped[grouper(row)].append(row)
    if value_transform is None:
        return grouped
    else:
        return { key : value_transform(rows)
                 for key, rows in grouped.items() }
def picker(field_name):
    """returns a function that picks a field out of a dict"""
    return lambda row: row[field_name]
def pluck(field_name, rows):
    """turn a list of dicts into the list of field_name values"""
    return map(picker(field_name), rows)
def day_over_day_changes(grouped_rows):
    """sort the rows by date and zip with an offset to get pairs of consecutive days"""
    ordered = sorted(grouped_rows, key=picker("date"))
    return [{   "symbol"    : today["symbol"],
                "date"      : today["date"],
                "change"    : (today["price_usd"] / yesterday["price_usd"] - 1)
    } for yesterday, today in zip(ordered, ordered[1:])]


# Get the Max and Min price for Sol and Btc 
max_sol_price = max(row['price_usd'] for row in data if row['symbol'] == 'SOL')
min_sol_price = min(row['price_usd'] for row in data if row['symbol'] == 'SOL')
max_btc_price = max(row['price_usd'] for row in data if row['symbol'] == 'BTC')
min_btc_price = min(row['price_usd'] for row in data if row['symbol'] == 'BTC')

# Find min and max changes values over one day period
changes_by_symbol = (group_by(picker("symbol"), data, day_over_day_changes))

max_change_by_symbol = {}
min_change_by_symbol = {}

for symbol, changes in changes_by_symbol.items():
    max_change = max(changes, key=picker("change"))
    min_change = min(changes, key=picker("change"))
    max_change_by_symbol[symbol] = max_change
    min_change_by_symbol[symbol] = min_change

for symbol, change in max_change_by_symbol.items():
    print(f"{symbol} : {change}")

for symbol, change in min_change_by_symbol.items():
    print(f"{symbol} : {change}")


# Calculate consecutive days with less than 2% change
consecutive_days = {}
for symbol, changes in changes_by_symbol.items():
    max_consecutive_days = 0
    current_consecutive_days = 0
    
    for change in changes:
        if abs(change["change"]) > 0.05:
            current_consecutive_days += 1
        else:
            if current_consecutive_days > max_consecutive_days:
                max_consecutive_days = current_consecutive_days
            current_consecutive_days = 0

    # Final check in case the longest streak ends on the last day
    if current_consecutive_days > max_consecutive_days:
        max_consecutive_days = current_consecutive_days
    
    consecutive_days[symbol] = max_consecutive_days

# Output the result
for symbol, days in consecutive_days.items():
    print(f"{symbol}: {days} consecutive days with less than 2% change")

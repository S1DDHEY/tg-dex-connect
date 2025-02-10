import requests
import json
import csv
import os

def fetch_pair_data(pair_address):
    """Fetch data for a given pair from Dex Screener API, save JSON data,
    and write a CSV file with the base token's symbol and address."""
    
    # Ensure the data folder exists
    os.makedirs('./data', exist_ok=True)
    
    url = f"https://api.dexscreener.com/latest/dex/search?q={pair_address}"
    json_file = f"./data/{pair_address}.json"
    csv_file = "./data/coin_data.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Check if any pairs were returned
        if 'pairs' not in data or not data['pairs']:
            print(f"No data found for {pair_address}")
            return False

        # Save the JSON data to a file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"New coin found! Data saved to {json_file}.")
        
        # Write the CSV file with headers and base token data
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header row
            writer.writerow(['symbol', 'address'])
            
            # Iterate over each pair and extract baseToken info
            for pair in data['pairs']:
                base_token = pair.get('baseToken', {})
                symbol = base_token.get('symbol', '')
                address = base_token.get('address', '')
                writer.writerow([symbol, address])
                
        print(f"CSV file created at {csv_file}.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"API request failed for {pair_address}:", e)
        return False

# Example usage
fetch_pair_data("DhvE9DWxJBM9AuZ5hNDQEKWPsDb9kwdY9z6zKYbdfart")

import pandas as pd
import os

# Folder where CSV files are located
data_folder = 'data'

# Output list to store all filtered DataFrames
all_data = []

# Loop through each file in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(data_folder, file_name)

        # Read CSV
        df = pd.read_csv(file_path)

        # Filter for Pink Morsel
        df = df[df['product'] == 'Pink Morsel']

        # Calculate sales
        df['sales'] = df['quantity'] * df['price']

        # Keep only sales, date, region
        df = df[['sales', 'date', 'region']]

        # Add to list
        all_data.append(df)

# Combine all into one DataFrame
final_df = pd.concat(all_data)

# Save to a new CSV
final_df.to_csv('filtered_sales.csv', index=False)

print(" Data processed and saved to 'filtered_sales.csv'")

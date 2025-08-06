import csv
import os

DATA_DIRECTORY = "./data"           # Folder containing your CSV files
OUTPUT_FILE_PATH = "./filtered_sales.csv"    # Output CSV file

def process_files(data_dir, output_file):
    header = ["sales", "date", "region"]

    with open(output_file, mode='w', newline='', encoding='utf-8') as output_fp:
        writer = csv.writer(output_fp)
        writer.writerow(header)

        # Loop through all files in the data directory
        for file_name in os.listdir(data_dir):
            file_path = os.path.join(data_dir, file_name)

            # Only process CSV files
            if not file_name.lower().endswith('.csv'):
                continue

            with open(file_path, mode='r', encoding='utf-8') as input_fp:
                reader = csv.reader(input_fp)

                # Skip header row and process data rows
                next(reader, None)

                for row in reader:
                    if len(row) < 5:
                        # Skip rows with insufficient columns
                        continue

                    product = row[0].strip()
                    raw_price = row[1].strip()
                    quantity = row[2].strip()
                    transaction_date = row[3].strip()
                    region = row[4].strip().lower()  # Normalize region to lowercase to match Dash filtering

                    if product == "pink morsel":
                        try:
                            # Remove $ sign if present and convert price and quantity properly
                            price = float(raw_price.replace('$', ''))
                            qty = int(quantity)
                            sale = price * qty

                            # Write to output file: sales, date, region
                            writer.writerow([sale, transaction_date, region])
                        except ValueError:
                            # Handle any conversion problems
                            print(f"Skipping row due to conversion error: {row}")
                            continue

if __name__ == "__main__":
    process_files(DATA_DIRECTORY, OUTPUT_FILE_PATH)
    print(f"Filtered sales data successfully written to {OUTPUT_FILE_PATH}")

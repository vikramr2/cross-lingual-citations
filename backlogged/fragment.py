import pandas as pd
import os
import sys

def split_csv(input_file, rows_per_file, output_folder):
    # Create the output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Load the CSV file
    data = pd.read_csv(input_file)

    # Calculate the number of chunks to be created
    total_rows = data.shape[0]
    number_of_files = (total_rows + rows_per_file - 1) // rows_per_file

    # Split the dataframe into chunks and save each to a new CSV file in the specified folder
    for i in range(number_of_files):
        start_row = i * rows_per_file
        end_row = start_row + rows_per_file
        # Create a slice of the dataframe for the current chunk
        chunk = data.iloc[start_row:end_row]
        # Define the output file path
        output_file = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(input_file))[0]}_part_{i+1}.csv')
        # Save the chunk to a new CSV file
        chunk.to_csv(output_file, index=False)
        print(f'Created: {output_file}')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <rows_per_file> <output_folder>")
        sys.exit(1)

    input_file = sys.argv[1]
    rows_per_file = int(sys.argv[2])
    output_folder = sys.argv[3]

    split_csv(input_file, rows_per_file, output_folder)

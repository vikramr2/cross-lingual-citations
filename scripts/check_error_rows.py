import csv

def count_single_integer_rows(file_path):
    # Initialize a counter for rows with only one integer
    single_integer_count = 0
    
    # Open the TSV file
    with open(file_path, newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        
        # Iterate over each row in the TSV file
        for row in reader:
            # Filter out empty strings and count non-empty fields
            non_empty_fields = sum(1 for field in row if field.strip())
            
            # Check if there is exactly one non-empty field
            if non_empty_fields == 1:
                single_integer_count += 1
    
    return single_integer_count

# Example usage
file_path = 'oc_citation_events_last_5yrs_int_el.tsv'  # Replace 'your_file.tsv' with your file path
result = count_single_integer_rows(file_path)
print(f'The number of rows with only one integer is: {result}')

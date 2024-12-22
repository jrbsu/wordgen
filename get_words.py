import csv
from modules import utils

def get_sorted_unique_values_from_tsv(file_path):
    unique_values = set()
    
    with open(file_path, 'r', newline='', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        
        next(reader)
        
        for row in reader:
            first_column_value = row[0].strip()
            second_column_value = row[1].strip()
            
            if first_column_value and second_column_value != "—" and "suff." not in second_column_value:
                unique_values.add(first_column_value)
    
    sorted_unique_values = sorted(unique_values)
    
    return sorted_unique_values

file_path = 'materials/data.tsv'
sorted_unique_values = get_sorted_unique_values_from_tsv('materials/data.tsv')
print(sorted_unique_values)

for word in sorted_unique_values:
    out = utils.stress(word, word, True)
    print(out)


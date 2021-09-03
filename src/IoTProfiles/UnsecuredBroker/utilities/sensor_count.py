import csv

# 11939728 lines
file_name_path # Fill in the file name
with open(f'{file_name_path}') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    data = []
    for row in csv_reader:
        if row[1] not in data:
            data.append(row[1])
        line_count += 1
    print(f'FOund {line_count} sensors.\n')
    print(data)

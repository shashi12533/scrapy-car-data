import csv
import json
with open('SearchEngineScrapy/file/file5.json','r') as f:
    data = json.loads(f.read())

print(data)
csv_columns=[]
max1=0
for i in data:
    if len(i.keys())>max1:
        csv_columns=[]
        csv_columns.extend((i.keys()))

print(len(csv_columns))
# try:
#     with open('ciaz.csv', 'a') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
# except Exception as e:
#     print(str(e))

#$$$$$$$$$$$$$$$$









# print(csv_columns)
#
for i in data:
    try:
        with open('ciaz.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            # writer.writeheader()
            writer.writerow(i)
    except Exception as e:
        import pdb
        pdb.set_trace()
        print(i)


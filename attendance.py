import csv

with open('data.csv', 'w', newline='') as f:
	writer = csv.writer(f)

	writer.writerow([''])
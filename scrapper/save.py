import csv


def save_to_file(jobs):
    f = open('jobs.csv', 'w', newline='', encoding='UTF-8')
    writer = csv.writer(f)
    writer.writerow(['Title', 'Company', 'Location', 'Link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return

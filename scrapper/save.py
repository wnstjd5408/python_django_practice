import csv


def save_to_file(jobs):
    f = open('jobs.csv', 'w', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    writer.writerow(['Index', 'Company', 'Spec',
                     'Location', 'Content', 'Link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return


# def save_to_jobskorea(jobs):
#     f = open('jobskorea.csv', 'w', newline='', encoding='UTF-8')
#     writer = csv.writer(f)
#     writer.writerow(['Company', 'Spec', 'Location', 'Content', 'Link'])
#     for job in jobs:
#         writer.writerow(list(job.value()))
#     return

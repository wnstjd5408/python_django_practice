from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stackoverflow_jobs
from save import save_to_file


indeed_jobs = get_indeed_jobs()
so_jobs = get_stackoverflow_jobs()


jobs = indeed_jobs + so_jobs


save_to_file(jobs)

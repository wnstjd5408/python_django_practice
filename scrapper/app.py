from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs as get_stackoverflow
from save import save_to_file, save_to_jobskorea
from jobkorea import get_jobs as get_jobkorea

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobkorea(word)
            db[word] = jobs
    else:
        return redirect('/')
    return render_template("report1.html",
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_jobskorea(jobs)
        return send_file("jobskorea.csv")
    except:
        return redirect('/')


if __name__ == '__main__':
    app.run()

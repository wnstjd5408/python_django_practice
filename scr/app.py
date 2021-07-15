from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs as get_stackoverflow
from save import save_to_file
from jobkorea import get_jobs as get_jobkorea
from sqlite33 import jobskorea_insert

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
        save_to_file(jobs, word)
        return send_file(f"{word}.csv",
                         mimetype='text/csv',
                         as_attachment=True,
                         attachment_filename=f"{word}.csv")

    except:
        return redirect('/')


@app.route("/commit")
def commit():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()

        jobs = db.get(word)
        if not jobs:
            raise Exception()

        # for job in jobs:
        #     print(job)
        jobskorea_insert(jobs)
        return render_template('finish.html')

    except:
        return redirect('/')


if __name__ == '__main__':
    app.run()

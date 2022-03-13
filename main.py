"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from scraper_so import get_jobs as jobs_so
from scraper_wwr import get_jobs as jobs_wwr
from scraper_rok import get_jobs as jobs_rok
from download import save_to_file

app = Flask("job_scraper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('keyword').lower().strip()
  jobs = jobs_so(word+"+remote")
  try:
    jobs.extend(jobs_rok(word))
  except:
    pass
  jobs.extend(jobs_wwr(word))
    
  if jobs == []:
    return redirect("/fail")
  else:
    db[word] = jobs
  return render_template(
    "report.html", 
    no_results=len(jobs), 
    search_word=word, 
    jobs=jobs
    )

@app.route("/fail")
def fail():
  return render_template("fail.html")

@app.route("/export")
def export():
  print("exporting")
  try:
    word = request.args.get('keyword')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    filename = word + ".csv"
    print(filename)
    return send_file(filename, as_attachment=True, attachment_filename=filename, cache_timeout=0)
  except:
    return redirect("/")


app.run(host="0.0.0.0")
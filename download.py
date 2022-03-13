import csv

def save_to_file(jobs, word):
  filename = word + ".csv"
  file = open(filename, mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "link"])
  print("writing")
  for job in jobs:
    writer.writerow(list(job.values()))
  return
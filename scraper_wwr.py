import requests as r
import re
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://weworkremotely.com"

def extract_jobs(search_keyword):
  jobs = []
  result = r.get(f"{URL}/remote-jobs/search?term={search_keyword}")
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find("div",{"class":"jobs-container"}).find_all(href=re.compile("/remote-jobs"))
  
  for result in results:
    company = result.find("span",{"class":"company"}).text
    title = result.find("span",{"class":"title"}).text
    link = result["href"]
    jobs.append({"title":title, "company": company, "link": f"{URL}{link}"})
  return jobs

def get_jobs(search_keyword):
  print(f"Scraping weworkremotely.com for {search_keyword} jobs")
  jobs = extract_jobs(search_keyword)
  return jobs
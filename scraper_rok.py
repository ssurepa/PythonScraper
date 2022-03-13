import requests as r
import re
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

URL = "https://remoteok.io"

def extract_jobs(search_keyword):
  jobs = []
  html = r.get(f"{URL}/remote-{search_keyword}-jobs", headers = headers)
  soup = BeautifulSoup(html.text, "html.parser")
  results = soup.find("div",{"class":"container"}).find_all("tr",{"class":"job"})
  
  for result in results:
    company = result.find("span",{"class":"companyLink"}).text.strip()
    title = result.find("h2",{"itemprop":"title"}).text.strip()
    link = result["data-href"]
    jobs.append({"title":title, "company": company, "link": f"{URL}{link}"})
  return jobs

def get_jobs(search_keyword):
  print(f"Scraping remoteok.com for {search_keyword} jobs")
  try:
    jobs = extract_jobs(search_keyword)
    return jobs
  except:
    print("Keyword doesn't exist in remoteok.io. Please try a different keyword.")
    return
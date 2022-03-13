import requests as r
from bs4 import BeautifulSoup


URL = "https://stackoverflow.com"

def extract_pages(search_keyword):
  result = r.get(f"{URL}/jobs?q={search_keyword}")
  soup = BeautifulSoup(result.text, "html.parser")
  try:
    links = soup.find("div",{"class":"s-pagination"}).find_all('a')
  except:
    last_page = 1
    return last_page
    
  last_page = int(links[-2].text.strip())
  
  return last_page

def extract_jobs(last_page, search_keyword):
  jobs = []

  for page in range(last_page):
    result = r.get(f"{URL}/jobs?q={search_keyword}&pg={page + 1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div",{"class":"-job"})

    for result in results:
      title = result.select_one("a[title]").text
      company, location = result.find("h3").find_all("span", recursive=0)
      job_id = result.find("h2").find("a")["href"]
      jobs.append({
        "title":title,
        "company": company.text.strip(),
        "link": f"{URL}{job_id}"
      })

  return jobs

def get_jobs(search_keyword):
  print(f"Scraping stackoverflow.com for {search_keyword} jobs")
  last_page = extract_pages(search_keyword)
  if last_page == 0:
    jobs = []
  else:
    jobs = extract_jobs(last_page, search_keyword)
  return jobs
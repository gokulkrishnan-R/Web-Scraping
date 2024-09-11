#A simple web scraping projects:
"""
import requests as request
from bs4 import BeautifulSoup

class movies_website():
	def __init__(self,url,headers,book_lists,a,book_names):
		self.url=url
		self.headers=headers
		self.soup=BeautifulSoup(self.url.text,"lxml.parser")
		self.book_lists=book_lists
		
		print("Pls wait here....")

	def _get_soup_(self):
		return("Passed Out!")

	def get_movie_details(self):

		self.book_lists=self.a.find(name="li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

		for self.books_names in self.book_lists:
			self.book_title=self.books_names.find_all(name="h3").get_text()
			return self.book_title
			
movie_links=movies_website(request.get("https://books.toscrape.com/"),{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"},"","","")
print("The output is",movie_links.get_movie_details)
"""

#//////// Chat gpt's code aeomse /////////
import requests
from bs4 import BeautifulSoup

class MoviesWebsite:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.soup = self._get_soup()

    def _get_soup(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print("Failed to retrieve the webpage.")
            return None

    def get_movie_details(self):
        if self.soup is None:
            return "Soup is not initialized."

        book_lists = self.soup.find_all(name="li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        details = []
        for book in book_lists:
            book_title = book.find(name="h3").get_text()
            details.append(book_title)
        return details

url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
movie_links = MoviesWebsite(url, headers)

print("The output is", movie_links.get_movie_details())


import requests as request
from bs4 import BeautifulSoup
from lxml import *

class all_jobs():

    def __init__(self, url, headers):
        self.url = url    
        self.headers = headers
        self.soup = self._get_soup()
    
    def _get_soup(self):
        response = request.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return BeautifulSoup(response.content, "lxml")
        else:
            print("Failed to retrieve the page!")
            return None
    
    def get_job_details(self):
        if self.soup is None:
            return "The SOUP is not initialized properly!"
        
        job_lists = self.soup.find_all(name="li", class_="clearfix job-bx wht-shd-bx")
        details = []
        
        for job in job_lists:
            job_title = job.find(name="h2").text.strip()
            company_name = job.find(name="h3", class_="joblist-comp-name").text.strip()
            company_location = job.find(name="span").text
            job_link = job.find(name="a").get("href").strip()
            job_posted_date = job.find(name="span", class_="sim-posted").text.strip()
            experience = job.find(name="li").get_text()[-9:].strip()
            job_description = job.find(name="ul", class_="list-job-dtl clearfix").get_text().replace("\n", "")
            
            details.append({
                "Job Title": job_title,
                "Company Name": company_name,
                "Company Location": company_location,
                "Job Link": job_link,
                "Job Posted Date": job_posted_date,
                "Experience": experience,
                "Job Description": job_description
            })

        if not details:
            return "No job details found."
        
        return details

url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python&txtKeywords=Python&txtLocation=Chennai&cboWorkExp1=0"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
job_dashboard = all_jobs(url, headers)

job_details = job_dashboard.get_job_details()

# Print each job detail in a formatted way
if isinstance(job_details, list):
    for job in job_details:
        print(f"Job Title: {job['Job Title']}")
        print(f"Company Name: {job['Company Name']}")
        print(f"Company Location: {job['Company Location']}")
        print(f"Job Link: {job['Job Link']}")
        print(f"Job Posted Date: {job['Job Posted Date']}")
        print(f"Experience: {job['Experience']}")
        print(f"Job Description: {job['Job Description']}")
        print("\n")
else:
    print(job_details)
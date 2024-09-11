# /// Virtual Environment name == "jobs" ///

import requests as request
from bs4 import BeautifulSoup
from lxml import *
import sqlite3 as sqlite
import pandas as pd

class all_jobs():

    def __init__(self,url,headers):
        self.url=url    
        self.headers=headers
        self.soup=self._get_soup()
        self.db_name="jobs.db" #Creating a database file here
        self.table_name="job_details" #Creating the table too
        self.create_db_table()
        #self.convert_into_csv()
        #self.sno=sno

    def create_db_table(self):
        with sqlite.connect(self.db_name) as conn:
            cursor=conn.cursor()
            cursor.execute(f""" 
            CREATE TABLE IF NOT EXISTS {self.table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT,
                company_name TEXT,
                company_location TEXT,
                job_link TEXT,
                job_posted_date TEXT,
                experience TEXT,
                job_description TEXT
                )
                """)
            conn.commit() #Commiting all the required sqlite3 files.
    
    def _get_soup(self):
        response=request.get(self.url,self.headers)
        if response.status_code == 200:
            return BeautifulSoup(response.content,"lxml")
        else:
            print("Failed to retrive the message from the page!")
            return None
            
    def get_job_details(self):
        if self.soup is None:
            return "The SOUP is not initialized properly!"
        else:
            job_lists=self.soup.find_all(name="li",class_="clearfix job-bx wht-shd-bx")
            details=[]
            #sno=0
            for job in job_lists:
                '''#job_title=job.h2.a.find(name="strong",class_="blkclor").get_text().strip()
                job_title=job.find(name="h2").get_text()[:-1].replace("\n","")
                company_name=job.find(name="h3", class_="joblist-comp-name").get_text().strip()
                company_location=job.find(name="span",title="Chennai").get_text().strip()
                job_link=job.find(name="a").get("href").strip()
                job_posted_date=job.find(name="span",class_="sim-posted").get_text().strip()
                experience=job.find(name="li").get_text()[-9:].strip()
                job_description=job.find(name="ul",class_="list-job-dtl clearfix").get_text()[16:].strip().replace("\n","")
                '''
                job_title = job.find(name="h2").text.strip()
                company_name = job.find(name="h3", class_="joblist-comp-name").text.strip()
                company_location = job.find(name="span").text
                job_link = job.find(name="a").get("href").strip()
                job_posted_date = job.find(name="span", class_="sim-posted").text.strip()
                experience = job.find(name="li").get_text()[-9:].strip()
                job_description = job.find(name="ul", class_="list-job-dtl clearfix").get_text().replace("\n", "")
                
                details.append({"Job Title":job_title,
                                "Company Name": company_name,
                                "Company Location": company_location,
                                "Job Link": job_link,
                                "Job Posted Date": job_posted_date,
                                "Experience": experience,
                                "Job Description": job_description
                                })
            #self.sno+=1
                
            if not details:
                return "No job details found!"
            else:
                return details
            #print("\n")
            #return(f"Job Title:{job_title.strip()}\nCompany Name:{company_name}\nCompany_Location:{company_location}\nJob_Link:{job_link}\nJob_Posted_Date:{job_posted_date}\nExperience:{experience}\nJob_Description:{job_description}")

    def _insert_into_db(self,job_title,company_name,company_location,job_link,job_posted_date,experience,job_description):
        with sqlite.connect(self.db_name) as conn:
            cursor=conn.cursor()
            cursor.execute(f'''
            INSERT INTO {self.table_name} 
            (job_title,company_name,company_location,job_link,job_posted_date,experience,job_description) 
            VALUES (?,?,?,?,?,?,?) 
            ''',(job_title,company_name,company_location,job_link,job_posted_date,experience,job_description))
            conn.commit()

    """def convert_into_csv(self):
        with open("job_details.csv",w+) as self.f:
            """

url="https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python&txtKeywords=Python&txtLocation=Chennai&cboWorkExp1=0"
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
job_dashboard=all_jobs(url,headers)

job_details=job_dashboard.get_job_details()

if isinstance(job_details,list):
    for job in job_details[::]:
        print(f"Job Title:{job['Job Title']}\n")
        print(f"Company Name:{job['Company Name']}\n")
        print(f"Company Location:{job['Company Location']}\n")
        print(f"Job Link:{job['Job Link']}\n")
        print(f"Job Posted Date:{job['Job Posted Date']}\n")
        print(f"Experience:{job['Experience'][:-70]}\n")
        print(f"{job['Job Description']}\n")
    #else:
        #print("The below are job details",job_details)

      # Inserting each job into the database
        job_dashboard._insert_into_db(
            job["Job Title"],
            job["Company Name"],
            job["Company Location"],
            job["Job Link"],
            job["Job Posted Date"],
            job["Experience"],
            job["Job Description"]
        )
    
    #EXporting al details to excel(csv files)
    df=pd.DataFrame(job_details)
    df.to_excel("Job_Details.xlsx",index=False,engine="openpyxl")
    print(f"All job details have been exported to the file: Job_Details.xlsx")

    #Writing the job details in txt file format too.
    with open("job_full_datas.txt", "w") as f:
        for serialnum,job in enumerate(job_details,start=1):
            f.write(f"S.No): {serialnum}\n")
            f.write(f"Job Title:{job['Job Title']}\n")
            f.write(f"Company name:{job['Company Name']}\n")
            f.write(f"Company location:{job['Company Location']}\n")
            f.write(f"Job link:{job['Job Link']}\n")
            f.write(f"Job posted date:{job['Job Posted Date']}\n")
            f.write(f"Job description:{job['Job Description']}\n")
            f.write("\n" + "="*50 + "\n\n")
            
#a="Job Description:Perks  & amp; Benefits Salary:Rs 2.5 Lacs - 4 Lacs p.a"
#print(len(a))

"""def db_connection():
        conn=sqlite.connect("job_dbs.db")
        cur=conn.cursor()
"""
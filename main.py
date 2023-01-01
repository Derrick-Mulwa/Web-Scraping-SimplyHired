# Import important libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


# I have created important functions first, and arranged the inthe right order at the bottom part of this code
# The get_jobTitle() function fetches the job Title from the page and returns it.

def get_jobTitle():
    try:
        job_title = page_information.find("div", class_="viewjob-jobTitle h2").text
    except:
        jobtitle = None

    return job_title


# The get_companyName() function fetches the hiring company's name and Company's Rating from the page
# and returns it. If the page has no company name, it returns None

def get_companyName_and_Rating():
    try:
        company_info = page_information.find_all("div", class_="viewjob-labelWithIcon")[0].text
        for i in range(len(company_info)):
            if company_info[i] == "-":
                company_name = (company_info[:i]).strip()
                rating = (company_info[i + 1:]).strip()

        if len(rating) == 0:
            rating = None


    except:
        company_name = None
        rating = None

    return company_name, rating


# The get_jobLocation() function below fetches the company's location. It returns the city and state where
# the company is from. If the job has only one location where city and state are not explicitly defined,
# it is considers the location as both the city and state

def get_jobLocation():
    try:
        company_location = page_information.find_all("div", class_="viewjob-labelWithIcon")[1].text

        if "," in company_location:
            position_of_comma = company_location.index(",")
            company_location_city = company_location[:position_of_comma].strip()
            company_location_state = company_location[position_of_comma + 1:].strip()
        else:
            company_location_city = company_location
            company_location_state = company_location


    except:
        company_location_city = company_location
        company_location_state = company_location

    return company_location_city, company_location_state


# The get_jobSalary() function below fetches the upbound and lowbound salary range, currency,
# time period(yearly or monthly), and if it is explicitly defined by the company or estimated

def get_jobSalary():
    try:
        salary = page_information.find("span", class_="viewjob-labelWithIcon viewjob-salary").text.split()

        # Find if Salary listed is estimated or explicitly defined

        if 'Estimated:' in salary:
            salary_type = "Estimated"
            salary.pop(salary.index("Estimated:"))

        else:
            salary_type = "Explicitly Defined"

        # Find payment cycle of the salary

        if "year" in salary:
            payment_cycle = "Annually"
        elif "month" in salary:
            payment_cycle = "Monthly"
        elif "hour" in salary:
            payment_cycle = "Hourly"
        else:
            payment_cycle = "Not Defined"

        # Find the salary's lower and upper bound limits, and currency
        bounds = []
        for i in salary:
            if i.startswith(("$", "€", "£", "¥", "₣", "₹")) is True:
                bounds.append(i)

            currency = bounds[0][0]

            # Return an integer for the lower bound and upper bound limits, Remove all currency signs
            if len(bounds) >= 2:
                lBound = bounds[0].translate({ord(i): None for i in "$€£¥₣₹"})
                uBound = bounds[1].translate({ord(i): None for i in "$€£¥₣₹"})
            else:
                lBound = bounds[0].translate({ord(i): None for i in "$€£¥₣₹"})
                uBound = bounds[0].translate({ord(i): None for i in "$€£¥₣₹"})


    except:
        salary_type, payment_cycle, lBound, uBound, currency = [None for i in range(5)]

    return salary_type, payment_cycle, lBound, uBound, currency


# The function get_jobType() fetches the job type the company wants ie Full-Time, part-time.
# Some companies do not list the job type
def get_jobType():
    try:
        job_type = page_information.find("span", class_="viewjob-labelWithIcon viewjob-jobType").text
    except:
        job_type = None

    return job_type


# The function below fetches all the benefits the company offers and returns as a string
def get_jobBenefits():
    try:
        job_benefits = page_information.find("ul", class_="Chips").find_all("li", class_="viewjob-benefit")
        benefits = ""
        for i in job_benefits:
            benefits = benefits + i.text + ", "

        if len(benefits) < 5:
            benefits = None
        else:
            benefits = benefits[:-2]

    except:
        benefits = None

    return benefits


# The function get_jobQualifications() below returns all the qualifications and skills required for the job
def get_jobQualifications():
    try:
        job_qualifications = page_information.find("div",
                                                   class_="viewjob-section viewjob-qualifications viewjob-entities") \
            .find_all("li", class_="viewjob-qualification")
        qualifications = ""
        for i in job_qualifications:
            qualifications = qualifications + i.text + ", "

        if len(qualifications) < 5:
            qualifications = None
        else:
            qualifications = qualifications[:-2]

    except:
        qualifications = None

    return qualifications


# The get_full_job_description() function below returns a paragraph of the information that the employer
# has listed, like key responsibilities and some history of the company. All information that the employer wants the
# applicants to know is listed here

def get_full_job_description():
    try:
        job_description = page_information.find("div", class_="viewjob-jobDescription").text. \
            replace('Full Job Description', '').replace('Position Description:', '').replace('Job Description', '')

    except:
        job_description = None

    return job_description


# The lists below store the collected data so that they can be written orderly to a csv file

job_title_list = []
company_name_list = []
rating_list = []
company_location_city_list = []
company_location_state_list = []
salary_type_list = []
payment_cycle_list = []
lBound_list = []
uBound_list = []
currency_list = []
job_type_list = []
benefits_list = []
qualifications_list = []
job_description_list = []

# Combine all the functions in the most perfect order

pages_to_scrape = 50

print("Fetching requested data: ")
for i in tqdm(range(1, (pages_to_scrape + 1))):

    # The url will change every time it loops because i will change. i reresents page number

    url = f"https://www.simplyhired.com/search?q=data+analyst&sb=dd&pn={i}"

    # Get the page's contents using requests() and beautifulSoup()

    response = requests.get(url).content

    soup = BeautifulSoup(response, "lxml")

    # The jobs are ordered as list items in an unordered list.The unordered list belong to class "jobs"
    # The job details are in <article> of class "SerpJob"

    unordered_list = soup.find("ul", class_="jobs")
    articles = unordered_list.find_all("article", class_="SerpJob")

    for article in articles:
        to_job_link = article.find("a", class_="SerpJob-link card-link")["href"]
        full_link = f"https://www.simplyhired.com{to_job_link}"

        content = BeautifulSoup(requests.get(full_link).content, "html.parser")
        page_information = content.find("main", class_="row")

        job_title = get_jobTitle()
        company_name = get_companyName_and_Rating()[0]
        rating = get_companyName_and_Rating()[1]
        location = get_jobLocation()
        company_location_city = location[0]
        company_location_state = location[1]
        salary_details = get_jobSalary()
        salary_type, payment_cycle, lBound, uBound, currency = salary_details[0], salary_details[1], salary_details[2], \
                                                               salary_details[3], salary_details[4]
        job_type = get_jobType()
        job_benefits = get_jobBenefits()
        qualifications = get_jobQualifications()
        job_description = get_full_job_description()

        job_title_list.append(job_title)
        company_name_list.append(company_name)
        rating_list.append(rating)
        company_location_city_list.append(company_location_city)
        company_location_state_list.append(company_location_state)
        salary_type_list.append(salary_type)
        payment_cycle_list.append(payment_cycle)
        lBound_list.append(lBound)
        uBound_list.append(uBound)
        currency_list.append(currency)
        job_type_list.append(job_type)
        benefits_list.append(job_benefits)
        qualifications_list.append(qualifications)
        job_description_list.append(job_description)

print(f"Scraping {pages_to_scrape} pages: Done")


# Put all the collected data to a pandas dataframe

df1 = pd.DataFrame({
    "job_title": job_title_list,
    "company_name": company_name_list,
    "rating": rating_list,
    "company_location(city)": company_location_city_list,
    "company_location_state": company_location_state_list,
    "salary_type": salary_type_list,
    "payment_cycle": payment_cycle_list,
    "Salary Range From": lBound_list,
    "Salary range To": uBound_list,
    "currency": currency_list,
    "job_type": job_type_list,
    "job_benefits": benefits_list,
    "qualifications": qualifications_list,
    "job_description": job_description_list

})

# Save the data to a csv file

print("Saving fetched data to csv file (collected data.csv)")
try:
    tqdm(df1.to_csv("Collected data.csv"))
    print("Data saved successfully!!")
except:
    print("Could not save data to csv file. Close any open instance of the csv and try again.")
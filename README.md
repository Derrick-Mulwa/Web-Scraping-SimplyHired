# Welcome to the SimplyHired Data Analyst Job Scraper! 

This python program is designed to gather detailed information about data analyst job openings from multiple pages on the SimplyHired website. The program utilizes the BeautifulSoup library to scrape data from the website and store it in a csv file.


Before running this program, you will need to have the following libraries installed:
  * BeautifulSoup
  * Pandas
  * Requests
  * Termcolor 
  * Tqdm

Once the scraping is complete, the program will create a csv file called Colledted data.csv in the same directory as the program file. This csv file will contain the following information for each job posting:
  * Job title
  * Company name
  * Location (Both city and state or remote)
  * Job requirements
  * Job benefits
  * Salary (If explicitly defined or estimated)
  * Low bound and upper bound salary limit
  * Job description.
  
When you use the program for the second time, it may determine where it last reached and stop scraping, reducing duplication of records.
  
# Additional Notes
The program is designed to scrape data from the SimplyHired website, but the website structure may change in the future which could cause the program to break.
The program is set to scrape data from the "data analyst" job category, but can be modified to scrape data from other job categories by changing the URL in the url variable.

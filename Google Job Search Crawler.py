#=====================================================================
# NOTES
#=====================================================================
# - You need to download chromedriver.exe and place it in the same loation as script (https://sites.google.com/a/chromium.org/chromedriver/home)
# - You can change the sleep values based on your internet/computer speed
# - Running this script too often will lead to a 429 request status. This means you've ran it too often. Wait and run again later. This is more of an issue when coding than actually using as one has to run it quite often.
# - When opening file in Excel, use Data > From Text/CSV > File Origin = 605001: Unicode(UTF-8)

#=====================================================================
# Import Libraries
#=====================================================================
import requests # gets the information from the site
from bs4 import BeautifulSoup # html parser
from selenium import webdriver # handles the request and interactions(scrolling of infinite scroller and buttons)
import sys, os, time, csv, unidecode

#=====================================================================
# Bypass Blocking Variables
#=====================================================================

# Create headers & params in order to bypass blocking
headers = {
    'authority': 'https://www.google.com/',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome"; v="87"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': '_helmet_couch=eyJzZXNzaW9uX2lkIjoiNjgzNzhmMmNmNjI5OTcxNjI5NzU2ZWNmMTM5MzE5MmIiLCJidWNrZXRfaWQiOiJmNTk1ZGRhYy00ZmVhLTQ5NmYtODNkNS00OWQzODgzMWFhYTAiLCJsYXN0X3NlZW4iOjE1OTEyNjgwNTUsInZvbCI6MSwiX2NzcmZfdG9rZW4iOiI1a3Yxb3FKTmhXTCs1YUxzdjYzRFk3TlNXeGs5TlhXYmZhM0UzSmtEL0NBPSJ9--22dfbfe582c0f3a7485e20d9d3932b32fbfb721b',
    'if-none-match': 'W/"e6fb8187391e99a90270c2351f9d17cd"',
}

params = (
    ('o', '\u039C\u03C0\u03BF\u03C5\u03C1\u03BD\u03BF\u03CD\u03B6\u03B9 Guy Laroche Linda Red'),
)

#=====================================================================
# Define Global Variables
#=====================================================================

features_data = []

#=====================================================================
# Funtions
#=====================================================================

#..................................................................
# Connect to site and then parse the data
def connect_and_parse():

    # connect to the site
    url = "https://www.google.com/search?q=data+scientist+USA&oq=data+scientist+jobs&aqs=chrome..69i57j0i433i457j0i402l2j0i395l4.3309j1j1&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwi9557CpvjtAhVKUMAKHaRHBtgQutcGKAB6BAgDEAQ&sxsrf=ALeKk00B6n8gIck0u29yarMEgr_UT9CMhw:1609420484628#htivrt=jobs&htidocid=JJ-VDq0HcUDG-ZDNAAAAAA%3D%3D&fpstate=tldetail"
    result = requests.get(url, headers=headers, params=params)

    # check if connection was made properly
    print("Request status: " + str(result.status_code) + " (200=good)")

    # parse site with BeautifulSoup
    soup = BeautifulSoup(result.text,'lxml')

    # find left job postings
    # div = soup.findAll('div',{'jsname':"DVpPy", 'class': 'hide-focus-ring'})

    # start seledium (required for interactions)
    PATH = os.path.dirname(sys.argv[0]) + "\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=(PATH))
    driver.get(url)

    print("[x] Connected to site.")
    print("[x] Site parsed.")
    return[soup, driver]

#..................................................................
# Scroll the element that conttains the jobs on the left of the screen. 
# The element is using an infinite scroller, so the script has to scroll, wait for the jobs to load, then check if new jobs loaded and if so scroll again
def scrollJobs(soup, driver):

    print("[x] Busy scolling to load all jobs. (Give me a minute)")
    
    # find the scroll element
    scroll_div = driver.find_element_by_xpath('//*[@id="immersive_desktop_root"]/div/div[3]/div[1]')

    old_count = 0
    counter = 0
    all_jobs_loaded = False

    # while jobs are still loading after scrolling
    while all_jobs_loaded == False:
        
        # Scroll and wait 2 seconds so that the new elements can load
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div)
        time.sleep(2)

        # get left elements
        soup=BeautifulSoup(driver.page_source, 'lxml')
        div = soup.findAll('div',{'jsname':"DVpPy", 'class': 'hide-focus-ring'})

        #  checking if there are more jobs when scrolling down
        new_count = len(div)
        if(old_count == len(div)):
            all_jobs_loaded = True
        else:
            old_count = new_count
            counter += 1

    # Scroll back to the top (for some reason this is required in order to click each job in order to select the description)
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight*-' + str(counter) , scroll_div)
    
    print("[x] Scrolling complete.")
    return(div)

#..................................................................
# Get jobs on the left
def get_left_elements(div):
    # for each job, get the relevant information in the left element

    print("[x] Getting jobs in left div.")

    for x in div:
        role            = x.findAll('div', {'class': 'BjJfJf PUpOsf'})
        company         = x.findAll('div', {'class': 'vNEEBe'})
        location        = x.findAll('div', {'class': 'Qk80Jf'})
        via             = x.findAll('div', {'class': 'Qk80Jf'})
        date_posted     = x.findAll('span', {'class': 'SuWscb'})
        try:

            employment_type = x.findAll('span', {'class': 'SuWscb'})[1].text
        except:
            employment_type = "Not Stated"

        # append information to array
        features_data.append([
            role[0].text,
            company[0].text,
            location[0].text,
            (via[1].text).split("via ")[1],
            date_posted[0].text,
            employment_type,
            ""]) # this is a placeholder for the description which we get on the right-hand side of the page

    print("[x] All jobs' basic data captured.")  

#..................................................................
# Get the additional job details in the element on the right (per each job)
def get_right_elements(driver):

    print("[x] Getting detail for each job. (time to go make some coffee...)")  

    # xpath to jobs on left element
    left_div = driver.find_element_by_xpath('//*[@id="immersive_desktop_root"]/div/div[3]/div[1]')
    left_jobs = left_div.find_elements_by_xpath('.//*[@class="hide-focus-ring"]')

    # For each job on left element
    for cl in left_jobs:
        
        # click on the job
        cl.click()

        right_div = driver.find_element_by_xpath('//*[@id="gws-plugins-horizon-jobs__job_details_page"]/div')

        # get right elements
        soup=BeautifulSoup(driver.page_source, 'lxml')
        div = soup.findAll('div',{'class': 'pE8vnd avtvi'})

        counter = 0
        for x in div:
            
            # only capturing the following as we already captured the rest via the left element
            description         = x.findAll('span', {'class': 'HBvzbc'})[0].text

            # adding description to the rest of the features
            features_data[counter][6] = description
            counter += 1

    print("[x] Job details (finally) scrapped.")  

#..................................................................
# Once all  data is captured, export as a CSV 
def export_to_csv():
    
    with open('job_list.csv', 'w', newline='', encoding='utf-8') as f: 

        # creating column names
        fieldnames =["Role", "Company", "Location", "Via", "Date Posted", "Employment Type", "Description"]
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        
        # run through features and add each as a row
        for i in features_data:
            thewriter.writerow({"Role" : (i[0]), "Company" : (i[1]), "Location" : (i[2]), "Via" : (i[3]), "Date Posted" : (i[4]), "Employment Type" : (i[5]), "Description" : (i[6])})

    print("[x] All data exported to CSV.")  
    print("Script Finished")
    print("=============================")


#=====================================================================
# Call functions
#=====================================================================

soup, driver = connect_and_parse() # connect to site and parse the site
div = scrollJobs(soup, driver) # scroll through the jobs on the left in order to load all the jobs
get_left_elements(div) # once all jobs are loaded, get all the job information on the left of screen
get_right_elements(driver) # go into the detail of each job to get additional infomation
export_to_csv() # export captured data to a csv file
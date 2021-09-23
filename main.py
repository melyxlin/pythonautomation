#importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# extracting the information data
def extract_info():
    # url where we will extracting internship information from
    url = "https://github.com/pittcsc/Summer2022-Internships"
    # variable to assign the extracted content
    response = requests.get(url, timeout=10)
    # will "beautify" the extracted content so to easily get specific content
    soup = BeautifulSoup(response.content, 'html.parser')
    # get back the table of internships
    table = soup.find('table')

    # produce the columns of the final csv and the names of these columns
    columns = [] # array representing the columns
    table_headers = table.find('thead') # extracting the row with all the table headers
    table_header_row = table_headers.find('tr') # putting the table header row in an array
    th = table_header_row.find_all('th') # getting the headers
    row = [i.text for i in th] # extracting only the name of the headers
    row.append("Applied?") # adding a column that will represent if we have applied for the job yet
    columns = row # assigning the columns to the header row

    # extract the internship data
    jobs = []
    table_body = table.find('tbody') # gets back all internship data
    table_rows = table_body.find_all('tr') # array to represent each internship
    for tr in table_rows:
        td = tr.find_all('td') 
        row = [i.text for i in td] # gets only the text of the internship data
        row.append("") # appending a blank space for the applied column
        jobs.append(row) # appending to the jobs array
    return [columns, jobs]

# put data in to a csv
def convert_to_csv(data):
    df = pd.DataFrame(data[1])
    df.columns = data[0]
    df.to_csv('jobs.csv',index=False)


if __name__ == "__main__":
    data = extract_info()
    convert_to_csv(data)

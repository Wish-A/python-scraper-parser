# This code will scrape and format the contents from a page on Raidforums.
# See the .html for specific details

import csv
from bs4 import BeautifulSoup
import re
import os
import glob

print("*" * 80)
print ("Reading the scrapes...")

csvDataset = "PutFileNameHere.csv"
sourceDirectory = 'PutPathNameHere'
csvPath = os.path.join(sourceDirectory, csvDataset)

# Reading directory for HTML-files
fileList = os.listdir(sourceDirectory)
for fileName in glob.glob(os.path.join(sourceDirectory, "*.html")):
    with open(fileName) as htmlFile:
        soup = BeautifulSoup(htmlFile)

# Lists for the classes
forumPostScrapeDateTime = soup.find("div", {"class":"footer__datetime"})
forumPostSection = soup.find("span", {"class":"forum-info__name rounded"})
forumPostTitle = soup.findAll("span", {"class":"forum-display__thread-subject"})
forumPostAuthors = soup.findAll("span", {"class":"author smalltext"})
forumPostDateTime = soup.findAll("span", {"class":"forum-display__thread-date"})
forumPostLastResponded = soup.findAll("span", {"class":"lastpost smalltext"})
forumPostLastRespondedDateAndTime = soup.findAll("span", {"class":"lastpost smalltext"})
forumPostReplies = soup.findAll("a", {"href": lambda f: f and f.startswith('https://raidforums.com/misc.php?action=whoposted')})
forumPostViews = soup.findAll("td",{"class":"trow2 forumdisplay_regular hidden-sm","align":"center"})
forumPostStatus = soup.findAll("a", {"class":"forum-display__thread-prefix forum-display__thread-prefix--new-thread rounded"})
forumPostPageNumber = soup.find("span", {"class":"pagination_current"})

print("DONE!\n")
print("Parsing the scrapes...\n")

#This is only a test and won't show the real results, the real results will be shown in the dataset (.csv file)
x = 0
for author in forumPostAuthors:
    author = author.text.strip()
    author = author.replace('by', '')
    print ("Scraped", forumPostScrapeDateTime.text.strip(), "|", "Post Section:", forumPostSection.text.strip(),"|", "Page Number:", forumPostPageNumber.text.strip(), "|", "Title:", forumPostTitle[x].text.strip(), "|","OP_Nick:", author, "|", forumPostDateTime[x].text.strip(), "|", "Last Post Time:", forumPostLastResponded[x].text.strip(), "|", "Replies:", forumPostReplies[x].text.strip(), "|", "Views:", forumPostViews[x].text.strip(), "|","Status:", forumPostStatus[x].text.split(),"\n")
    x = x + 1

# Writing data to csv file
with open(csvPath, "w", newline="") as csvfile:
    headers = ["Scrape Time", "Forum Section", "Page Number", "Title", "Author", "Date/Time of Post", "Date/Time Last Responded","Last Post Responder", "Replies", "Views","Post Status"]
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    data = csv.writer(csvfile)
    data.writerow(("Scrape Time", "Forum Section", "Page Number", "Title", "Author", "Date/Time of Post", "Date/Time Last Responded","Last Post Responder", "Replies", "Views", "Post Status"))
    y = 0
    for i in forumPostAuthors:
        writer.writerow({"Scrape Time": forumPostScrapeDateTime.text.strip().replace('Current time:',''), "Forum Section": forumPostSection.text.strip(), \
            "Page Number": forumPostPageNumber.text.strip(), "Title": forumPostTitle[y].text.strip(), \
                "Author": forumPostAuthors[y].text.strip().replace('by',''), "Date/Time of Post": forumPostDateTime[y].text.strip(), \
                    "Date/Time Last Responded": forumPostLastRespondedDateAndTime[y].text.strip().split(':')[0].replace('\n','').replace('Last Post',''), \
                        "Last Post Responder": forumPostLastResponded[y].text.strip().split(':')[-1], "Replies": forumPostReplies[y].text.strip(), \
                            "Views": forumPostViews[y].text.strip(), "Post Status": forumPostStatus[y].text.split()})
        y = y + 1

print("\nDONE!")
print("*" * 80)

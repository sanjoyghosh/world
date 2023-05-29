import re
import requests
import sys
from bs4 import BeautifulSoup

patternFull = re.compile("(agriculture: .*)(industry: .*)(services: .*)")
patternNA = re.compile("[a-z]*: NA")
patternPercent = re.compile("[a-z]*: (\d\d?\d?(?:\.\d)?)\% \((\d\d\d\\d)(?: est.)?\)")

# define the URL to download and parse
url = "https://www.cia.gov/the-world-factbook/field/gdp-composition-by-sector-of-origin"

# make a GET request to the URL
response = requests.get(url)
# check if the request was successful
if response.status_code == 200:
    # create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # print the title of the HTML document
    print(soup.title.string)
    print(len(soup.find_all("h2", "h3")))

    # print the body of the HTML document
    for item in soup.find_all("h2", "h3"):
        agriculturePercent = -1.0
        agricultureYear = -1
        industryPercent = -1.0
        industryYear = -1
        servicesPercent = -1.0
        servicesYear = -1

        # print(item.text)
        # print(item.next_sibling.text)
        # Compile RE into Pattern outside loop.
        # m = re.match("(agriculture: .*)(industry: [NA|[\d\d?\d?[\.\d]?\% \((\d\d\d\d|FY12/13)[ est\.)]\)))services: (NA|\d(\d)?(\d)?(\.\d)?\% \((\d\d\d\d|FY12/13)( est\.)?\))", item.next_sibling.text)
        matchFull = patternFull.search(item.next_sibling.text)
        if matchFull is None:
            # print(item.next_sibling.text[does_match.span()[0]:does_match.span()[1]])
            # item.next_sibling.text[int(does_match.span()[0]), int(does_match.span()[1])]
            print(item.text)
            print(item.next_sibling.text)
            print("\n")
        else:
            country = item.text
            agricultureItem = matchFull.group(1)
            mAgricultureNA = patternNA.search(agricultureItem)
            if mAgricultureNA is not None:
                agriculturePercent = 0.0
                agricultureYear = 0
            else:
                mAgriculturePercent = patternPercent.search(agricultureItem)
                if mAgriculturePercent is not None:
                    agriculturePercent = float(mAgriculturePercent.group(1))
                    agricultureYear = int(mAgriculturePercent.group(2))
            industryItem = matchFull.group(2)
            mIndustryNA = patternNA.search(industryItem)
            if mIndustryNA is not None:
                industryPercent = 0.0
                industryYear = 0
            else:
                mIndustryPercent = patternPercent.search(industryItem)
                if mIndustryPercent is not None:
                    industryPercent = float(mIndustryPercent.group(1))
                    industryYear = int(mIndustryPercent.group(2))
            servicesItem = matchFull.group(3)
            mServicesNA = patternNA.search(servicesItem)
            if mServicesNA is not None:
                servicesPercent = 0.0
                servicesYear = 0
            else:
                mServicesPercent = patternPercent.search(servicesItem)
                if mServicesPercent is not None:
                    servicesPercent = float(mServicesPercent.group(1))
                    servicesYear = int(mServicesPercent.group(2))
        # Ignore Isle of Man.
        if item.text != "Isle of Man" and \
            (agriculturePercent < 0 or agricultureYear < 0 or 
             industryPercent < 0 or industryYear < 0 or 
             servicesPercent < 0 or servicesYear < 0):
            print("ERROR: " + item.text + " :: " + item.next_sibling.text)

else:
    # print an error message if the request was not successful
    print("Error:", response.status_code)
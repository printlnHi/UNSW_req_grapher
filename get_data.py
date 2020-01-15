import requests
from bs4  import BeautifulSoup as BS

UPPER_DIV_ID = 'readMoreSubjectConditions'

def get_course_reqs(code="COMP2521"):
  '''This function recieves a UNSW course code and returns the requisites to take the course
    At the moment it returns the whether the requisites are co-requisites (rather than pre-requisites and the unprocessed logical string detailing said requisites'''

  URL = f"https://www.handbook.unsw.edu.au/undergraduate/courses/2020/{code}/"
  response = requests.get(URL)
  soup = BS(response.text,'lxml')
  UPPER_DIV = soup.find(id=UPPER_DIV_ID)
  LOWER_DIV = UPPER_DIV.div.div
  text = LOWER_DIV.text
  print(text)

  '''The text we will get will be similar to one of the following::
      prerequisite: COMP 1511 or DPST1091 or COMP1917 or COMP1921
      Corequisite: MATH1131 or DPST1013 or MATH1141 or MATH1151
      Pre-requisite: MATH1081 AND COMP2521 AND (not enrolled in SENGAH)
      Prerequisite: COMP9024.
      
      the common sub-string to these is "requisite:".
      Thus the proposed algorithm is to split on this common substring, generating a left and right substring
      the right substrings will be examined to determine the nesting of courses
      the left substring will be examined to determine whether the requisite is pre or co

  '''

  left_ss, right_ss = text.split("requisite:")
  is_co = "co" in left_ss.lower()
  right_ss = right_ss.strip().strip(".").upper()
  return is_co,right_ss

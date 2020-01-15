import requests
from bs4  import BeautifulSoup as BS
import re
from course import Course

UPPER_DIV_ID = 'readMoreSubjectConditions'
CSV_NAME = "course_data.csv"

courses = {}

def get_course_reqs(code="COMP2521",courses={}):
  '''This function recieves a UNSW course code and returns the requisites to take the course
    At the moment it returns the whether the requisites are co-requisites (rather than pre-requisites and the unprocessed logical string detailing said requisites'''

  if code in courses:
    return courses[code].is_code,courses[code].req_ss

  URL = f"https://www.handbook.unsw.edu.au/undergraduate/courses/2020/{code}/"
  print(f" >Querying {URL}")
  response = requests.get(URL)
  #Many old courses which have been discontinued by UNSW are still listed as possible requisites for other courses. If we query them, the page returned will be 404. If this is the case, we return None from this function
  #TODO: Update thh function to check that the status code is 404, not just not ok
  if not response.ok:
    courses[code] = Course(code,is_recent=False)
    return None
  soup = BS(response.text,'lxml')
  UPPER_DIV = soup.find(id=UPPER_DIV_ID)

  #If a course has no requisites than UPPER_DIV will be None
  if UPPER_DIV == None:
    courses[code] = Course(code,req_ss="")
    return False,""

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
  courses[code] = Course(code,is_co=is_co,req_ss=right_ss)
  return is_co,right_ss


def iteratively_find_reqs(starting_courses = ["COMP6443"],prefix_blacklist=["DPST"]):
  '''This function will iteratively gather the information on all of the requisities of a given list of starting courses: effectively running a depth first search
    prefix_blacklist: any course which starts with a prefix in this blacklist will not be exploed as another courses requisite(but will be explored if in starting_courses)
  '''
  explored_courses = {}
  to_explore_stack = list(starting_courses)
  added_to_stack = set(starting_courses)
  #We are running a DFS w/ a stack rather than a BFS with a queue for ease of implementation
  #This choice is inconsequential

  while to_explore_stack:
    #Keep searching until the stack is exhausted
    exploring_code = to_explore_stack.pop()
    print(f"Exploring the course with code {exploring_code}")
    reqs = get_course_reqs(exploring_code)
    if reqs == None:
      print(f" >This course did not return a webpage, indicating it is discontinued")
      explored_courses[exploring_code]=None
      continue
    
    is_co,req_string = reqs

    print(f" >is_co = {is_co}, req_string = {req_string}")
    explored_courses[exploring_code]={"is_co":is_co,"req_string":req_string}

    #For now assume that the requisites are all simply this OR this OR this ...
    #We know string returner will be in upper case
    #TODO: Write code to parse the nested logical statements which UNSW can sometimes send us
    reqs = re.split(" *(OR|AND) *",req_string)

    #Remove OR and AND delimiters and iterate through
    for req in filter(lambda s: s not in ["OR","AND"],reqs):
      #If a requirement is one which we have not yet explored we add it to the stack
      if req not in added_to_stack and not any(prefix in req for prefix in prefix_blacklist):
        added_to_stack.add(req)
        to_explore_stack.append(req)


  return explored_courses

#iteratively_find_reqs()

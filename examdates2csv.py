#!/usr/bin/python3

import re
import sys
import urllib.request
from bs4 import BeautifulSoup
from collections import defaultdict

class Term:
  day : str
  month : str
  time : str
  lvl : str
  off : int


link = "http://www.fit.vutbr.cz/study/advisor/%s/zkousky%s/index.htm" % (sys.argv[1], sys.argv[2])
with urllib.request.urlopen(link) as url:
  s = url.read()

terms = defaultdict(list)

date = ""
soup = BeautifulSoup(s.decode("utf-8"), 'html.parser')
for tag in soup.find("table").find_all(["small", "td"]):
  if (tag.name == "small"):
    date = tag.text
  else:
    if re.match(re.compile("^[A-Z]{3}$"), tag.text):
      if date != "":
        try:
          t = Term()
          t.off = 0
          t.day = date.replace(' ', '').split('.')[0]
          t.month = date.replace(' ', '').split('.')[1]
          t.time = tag['colspan']
          t.lvl = tag['style'][18:-1]

          if t.lvl in ["99ff99", "FFC799", "FF9999"]:
            terms[tag.text].append(t)
            for sib in tag.previous_siblings:
              try:
                t.off += int(sib['colspan'])
              except:
                if sib.name == "td":
                  t.off += 1    
        except:
          None

print("Subject,Start Date,All Day Event,Start Time,End Time,Location,Description")
for key in terms:
  if any(x in key for x in sys.argv[3:]):
    for term in terms[key]:
      name = key
      if term.lvl == "99ff99":
        name += " - riadny termín"
      elif term.lvl == "FFC799":
        name += " - 1. opravný termín"
      if term.lvl == "FF9999":
        name += " - 2. opravný termín"

      if term.month == "12":
        year = sys.argv[1][:4]
      else:
        year = sys.argv[1][4:]

      print("\"%s\",%s/%s/%s,FALSE,%d:00,%d:50,," % 
        (name, term.month, term.day, year, 7 + int(term.off), 6+int(term.off)+int(term.time)))

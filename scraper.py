from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

'''
url = "https://www.basketball-reference.com/leagues/NBA_2020_standings.html"

html = urlopen(url)

soup = BeautifulSoup(html, features="lxml")

standings = soup.findAll('div',{'class':'standings_confs'})

standings = standings[0]

#print(standings.getText())
print(type(standings))

all_standings = standings.findAll('div',{'class':'table_wrapper'})

print(len(all_standings))
east_standing = all_standings[0]
west_standing = all_standings[1]

east_standing = east_standing.findAll('table')[0].findAll('tbody')[0]
west_standing = west_standing.findAll('table')[0].findAll('tbody')[0]
'''


def get_table(standing):
    names = [tr.findAll('th')[0].a.getText() for tr in standing.findAll('tr',{'class':'full_table'})]

    stats = [[td.getText() for td in row.findAll('td')] for row in standing.findAll('tr',{'class':'full_table'})]

    return zip(names,stats)

def get_standings(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

    html = urlopen(url)

    soup = BeautifulSoup(html, features="lxml")

    standings = soup.findAll('div',{'class':'standings_confs'})
    #print(standings)
    standings = standings[0]

    #print(standings.getText())
    print(type(standings))

    all_standings = standings.findAll('div',{'class':'table_wrapper'})

    print(len(all_standings))
    east_standing = all_standings[0]
    west_standing = all_standings[1]

    east_standing = east_standing.findAll('table')[0].findAll('tbody')[0]
    west_standing = west_standing.findAll('table')[0].findAll('tbody')[0]

    return get_table(east_standing),get_table(west_standing)

es,ws = get_standings('2016')

res = es
for r in res:
    print(r)
print('\n-------------------------------------')
res = ws
for r in res:
    print(r)

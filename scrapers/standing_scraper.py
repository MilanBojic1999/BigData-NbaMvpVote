from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd



def get_table(standing):
    names = [tr.findAll('th')[0].a.getText() for tr in standing.findAll('tr',{'class':'full_table'})]

    stats = [[td.getText() for td in row.findAll('td')] for row in standing.findAll('tr',{'class':'full_table'})]

    return zip(names,stats)

def get_standings(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

    html = urlopen(url)

    soup = BeautifulSoup(html, features="lxml")

    standings = soup.findAll('div',{'class':'standings_confs'})

    standings = standings[0]


    all_standings = standings.findAll('div',{'class':'table_wrapper'})

    east_standing = all_standings[0]
    west_standing = all_standings[1]

    east_standing = east_standing.findAll('table')[0].findAll('tbody')[0]
    west_standing = west_standing.findAll('table')[0].findAll('tbody')[0]

    east_table,west_table = get_table(east_standing),get_table(west_standing)

    result = []
    for team,stat in east_table:
        value = [team]+['E',year]+stat
        result.append(value)
    
    for team,stat in west_table:
        value = [team]+['W',year]+stat
        result.append(value)
    

    #res = sorted(res,key=lambda x: x[5])
    #res.reverse()

    headers = ['Name','Conference','Year','Wins','Losess','W/L%','GB','PS/G','PA/G','SRS']

    for r in result:
        r[5] = int(r[5][1:])/1000
        r[5] = "{:.3f}".format(r[5])
        r[6] = '0.0' if r[6] == '—' else r[6]
        #print(r)

    stand = pd.DataFrame(result,columns=headers)
    stand.to_csv(f"standings/standing_{year}.csv",index=False)


def call(start,end):

    for y in range(start,end):
        get_standings(y)
        print('Done year',y)
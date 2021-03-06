from urllib.request import urlopen
from bs4 import BeautifulSoup,Comment
import pandas as pd


def year_to_season(year):
    dd = year%100
    return '20'+ str(dd-1)+'-'+str(dd)

year = 2020

print(year_to_season(year))



def get_header():


    url = 'https://www.basketball-reference.com/players/j/jokicni01.html'

    html = urlopen(url)

    soup = BeautifulSoup(html, features="lxml")
    per_game = soup.find_all('table',{'id':'per_game'},limit=1)
    per_game = per_game[0]

    header = per_game.find_all('tr',limit=1)

    header = [th.getText() for th in header[0].find_all('th')]

    advanced = soup.find_all('table',{'id':'advanced'},limit=1)
    advanced = advanced[0]

    header2 = advanced.find_all('tr',limit=1)

    header2 = [th.getText() for th in header2[0].find_all('th')]


    full_header = ['Player']+header+header2[7:]
    for ind,h in enumerate(full_header):
        if h=='\xa0':
            print(ind)

    full_header = [h for h in full_header if h != '\xa0']
    
    return full_header


def get_stats(url,year):

    html = urlopen(url)

    soup = BeautifulSoup(html, features="lxml")

    name = soup.find_all('h1',{'itemprop':'name'},limit=1)

    name = name[0].span.getText()
    print(name)

    per_game = soup.find_all('table',{'id':'per_game'},limit=1)
    per_game = per_game[0]

    advanced = soup.find_all('table',{'id':'advanced'},limit=1)
    advanced = advanced[0]

    row1 = per_game.find_all('tr',{'id':f'per_game.{year}'},limit=1)[0]

    row1 = [tt.getText() for tt in row1.find_all(['th','td'])]


    row2 = advanced.find_all('tr',{'id':f'advanced.{year}'},limit=1)[0]

    exclue = {19,24}

    row2 = [tt.getText() for ind,tt in enumerate(row2.find_all(['th','td'])) if ind not in exclue]



    full_row = [name]+row1+row2[7:]

    #print(full_row)

    return full_row
    
def call():
    header = get_header()

    rows = []
    with open('player_stats/players_stats.txt','r') as f:
        for line in f:
            year,path = line.split(' ')
            rows.append(get_stats('https://www.basketball-reference.com'+path,int(year)))

    stand = pd.DataFrame(rows,columns=header)
    stand.to_csv("player_stats/player_stats.csv",index=False)


call()
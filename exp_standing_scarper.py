from os import name
from urllib.request import urlopen
from bs4 import BeautifulSoup,Comment
import pandas as pd

def get_header():
    url = "https://www.basketball-reference.com/leagues/NBA_2014_standings.html"

    html = urlopen(url)

    soup = BeautifulSoup(html, features="html.parser")

    #soup = soup.findAll('div',{'id':'all_expanded_standings'})

    for comment in soup(text=lambda it:isinstance(it,Comment)):
        if 'id="div_expanded_standings"' in comment.string:
            tag = BeautifulSoup(comment,'html.parser')
            comment.replace_with(tag)
            break

    standings = soup.findAll('div',{'id':'all_expanded_standings'})[0]

    standings = standings.findAll('table')[0].findAll('thead')[0]
    
    names = [th.getText() for th in standings.findAll('tr')[1].findAll('th')]
    names = names[:17]
    print(names)
    return names


head = get_header()

def get_standings(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
    # https://www.basketball-reference.com/leagues/NBA_2014_standings.html

    html = urlopen(url)

    soup = BeautifulSoup(html, features="html.parser")

    #soup = soup.findAll('div',{'id':'all_expanded_standings'})

    for comment in soup(text=lambda it:isinstance(it,Comment)):
        if 'id="div_expanded_standings"' in comment.string:
            tag = BeautifulSoup(comment,'html.parser')
            comment.replace_with(tag)
            break
    
    standings = soup.findAll('div',{'id':'all_expanded_standings'})[0]

    standings = standings.findAll('table')[0].findAll('tbody')[0]

    #rows = get_table(standings)
    rows = [[td.getText() for td in row.findAll('td')] for row in standings.findAll('tr')]
    
    result = []
    
    for ind,stats in enumerate(rows):
        tmp = [ind+1]+stats
        #print(name)
        result.append(tmp[:17])

    stand = pd.DataFrame(result,columns=head)
    stand.to_csv(f"exp_standings/standings_{year}.csv",index=False)


hh = []
for y in range(2000,2022):
    hh.append(get_standings(y))
    print('Done year',y)

from urllib.request import urlopen
from bs4 import BeautifulSoup,Comment
import pandas as pd


def get_table(table):
    table = table.findAll('tbody')[0]
    names = [tr.findAll('td')[0].a.getText() for tr in table.findAll('tr')]

    stats = [[td.getText() for td in row.findAll('td')[1:]] for row in table.findAll('tr')]

    return zip(names,stats)


def get_mvp_voting(year):

    url = f"https://www.basketball-reference.com/awards/awards_{year}.html#mvp"

    html = urlopen(url)

    soup = BeautifulSoup(html, features="lxml")


    mvp_table = soup.findAll('div',{'id':'div_mvp'})[0]

    mvp_table = mvp_table.findAll('table',{'id':'mvp'})[0]

    rows = get_table(mvp_table)
    
    result = []
    for name,stats in rows:
        tmp = [name,year]+stats
        result.append(tmp)

    for mini_r in result:
        for ind in range(10,20):
            if str(mini_r[ind]).startswith('.'):
                mini_r[ind] = '0'+mini_r[ind]
            elif mini_r[ind]=='':
                mini_r[ind] = '0.0'
        
    return result

def get_dpoy_voting(year):
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"

    html = urlopen(url)

    soup = BeautifulSoup(html, features="html.parser")

    for comment in soup(text=lambda it:isinstance(it,Comment)):
        if 'id="div_dpoy"' in comment.string:
            tag = BeautifulSoup(comment,'html.parser')
            comment.replace_with(tag)
            break

    dpoy_table = soup.findAll('div',{'id':"all_dpoy"})
    
    dpoy_table = dpoy_table[0]


    dpoy_table = soup.findAll('table',{'id':'dpoy'})[0]

    rows = get_table(dpoy_table)

    result = []
    for name,stats in rows:
        tmp = [name,year]+stats
        result.append(tmp)
    
    for mini_r in result:
        for ind in range(10,20):
            if str(mini_r[ind]).startswith('.'):
                mini_r[ind] = '0'+mini_r[ind]
            elif mini_r[ind]=='':
                mini_r[ind] = '0.0'
        
    return result

def get_votings(year):
    headers = ['Player','Year','Age','Team','FirstPlace','PtsWon','PtsMax','%','GP','MP','PTS','TRP','AST','STL','BLK','FG%','3P%','FT%','WS','WS/48']

    mvp = get_mvp_voting(year)
    dpoy = get_dpoy_voting(year)

    stand = pd.DataFrame(mvp,columns=headers)
    stand.to_csv(f"mvp_voting/mvp_{year}.csv",index=False)
    
    stand = pd.DataFrame(dpoy,columns=headers)
    stand.to_csv(f"dpoy_voting/dpoy_{year}.csv",index=False)



for y in range(2016,2022):
    get_votings(y)
    print('Done year',y)
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
    print(type(rows))
    for n,s in rows:
        print(n,s)

def get_dpoy_voting(year):
    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"

    html = urlopen(url)

    soup = BeautifulSoup(html, features="html.parser")

    dpoy_table = soup.findAll('div',{'id':"all_dpoy"})
    
    dpoy_table = dpoy_table[0]

    for element in dpoy_table(text=lambda it:isinstance(it,Comment)):
        element.extract()
        

    print(dpoy_table.prettify())
    ddd = dpoy_table.findAll('div')
    for d in ddd:
        if d.has_attr('id'):
            print(d['id'],d['class'])
        else:
            print(d['class'],'__',d.getText())

    #dpoy_table = dpoy_table.findAll('div',{'id':"div_dpoy"})[0]

    dpoy_table = soup.findAll('table',{'id':'dpoy'})[0]

    rows = get_table(dpoy_table)
    print(type(rows))
    for n,s in rows:
        print(n,s)

year = 2021

get_dpoy_voting(2021)
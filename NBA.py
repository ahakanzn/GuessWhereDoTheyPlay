import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

player_list=[]
alphabet='abcdefghijklmnopqrstuvwxyz'
root_list_page="https://www.basketball-reference.com/players/"
root_web_site="https://www.basketball-reference.com/"
for char in alphabet:
    r=requests.get(root_list_page+char+"/")
    soup=BeautifulSoup(r.content,"html.parser")
    player_temp=soup.select("th strong a")
    player_temp=[root_web_site+link.get("href") for link in player_temp]
    player_list.extend(player_temp)
    print(player_temp)
df=pd.DataFrame(columns=['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
       '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
       'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'İsim',
       'Boy', 'Kilo'])


def sezon(x):
    if type(x) is str:
        return bool(re.search("[0-9]{4}-[0-9]{2}",x))
    return False
for player in player_list:
    r = requests.get(player)
    soup = BeautifulSoup(r.content, "html.parser")

    table = str(soup.select_one("#all_per_game table"))
    table = pd.read_html(table)[0]
    temp_df = table[table["Season"].apply(sezon)].dropna(axis=1)

    isim = soup.select_one("h1[itemprop='name']").getText()
    boy = soup.select_one("span[itemprop='height']").getText()
    kilo = soup.select_one("span[itemprop='weight']").getText()
    dogum_tarihi = soup.select_one("span[itemprop='birthDate']").get("data-birth")

    temp_df["Boy"] = boy
    temp_df["Kilo"] = kilo
    temp_df["İsim"] = isim
    df=df.append(temp_df,ignore_index=True)
    print(isim)
print(df)
df.to_excel("output.xlsx")

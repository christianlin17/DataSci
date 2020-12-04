from sys import argv
from requests import get
import pandas as pd 
from bs4 import BeautifulSoup

rushingURL = """https://www.pro-football-reference.com/years/2020/opp.htm"""

urls = {
    'Rushing': rushingURL
}

dfs = []

defColumnSettings = {
    'axis': 1,
    'inplace': True
}

for key, url in urls.items():

    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # div = soup.find(lambda tag: tag.name=='div' and tag.has_attr('class') and tag['class']=='dataTables_wrapper no-footer')
    # table = div.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=='DataTables_Table_0')
    # rows = table.findAll(lambda tag: tag.name=='tr')
    # df = pd.read_html(str(table))[0]

print(soup)
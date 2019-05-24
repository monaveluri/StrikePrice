import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_base_url(Code):
    Base_url = ("https://www.nseindia.com/live_market/dynaContent/" +
            "live_watch/option_chain/optionKeys.jsp?symbolCode=-10003&symbol="+Code+"&" +
            "symbol="+Code+"&instrument=OPTIDX&date=-&segmentLink=17&segmentLink=17")
    return Base_url

def get_page_content(Code):
    Base_url = get_base_url(Code)
    html_page = requests.get(Base_url)
    html_page_content = BeautifulSoup(html_page.content, 'html.parser')

    table_cls_1 = html_page_content.find_all(id="octable")
    col_list = []

    # The code given below will pull the headers of the Option Chain table
    for mytable in table_cls_1:
        table_head = mytable.find('thead')

        try:
            rows = table_head.find_all('tr')
            for tr in rows:
                cols = tr.find_all('th')
                for th in cols:
                    er = th.text
                    ee = er.encode('utf8')
                    ee = str(ee, 'utf-8')
                    col_list.append(ee)

        except:
            print("no thead")

    col_list_fnl = [e for e in col_list if e not in ('CALLS', 'PUTS', 'Chart', '\xc2\xa0', '\xa0')]
    #print(col_list_fnl)

    table_cls_2 = html_page_content.find(id="octable")
    all_trs = table_cls_2.find_all('tr')
    req_row = table_cls_2.find_all('tr')

    new_table = pd.DataFrame(index=range(0, len(req_row) - 3), columns=col_list_fnl)
    row_marker = 0

    for row_number, tr_nos in enumerate(req_row):

        # This ensures that we use only the rows with values
        if row_number <= 1 or row_number == len(req_row) - 1:
            continue

        td_columns = tr_nos.find_all('td')

        # This removes the graphs columns
        select_cols = td_columns[1:22]

        for nu, column in enumerate(select_cols):
            utf_string = column.get_text()
            utf_string = utf_string.strip('\n\r\t": ')

            tr = utf_string.encode('utf-8')
            tr = str(tr, 'utf-8')
            tr = tr.replace(',', '')
            if(len(re.findall("-$",tr))):
                tr = tr.replace('-', '0')
            new_table.iloc[row_marker, [nu]] = tr

        row_marker += 1
    return new_table

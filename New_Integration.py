import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.animation as animation
from nsetools import Nse
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton



class App(QWidget):


    def __init__(self):
        super().__init__()
        self.title = 'Select a Stock'
        self.left = 200
        self.top = 200
        self.width = 200
        self.height = 200
        #self.move(-500,500)
        self.initUI()


    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.combo = QComboBox(self)
        nse = Nse()
        quoteCodeList = nse.get_index_list()
        #list_1 = ['Avengers']
        self.combo.move(0,60)
        self.combo.addItem("Select")
        self.combo.addItems(quoteCodeList)
        self.button = QPushButton("Ok", self)
        self.button.clicked.connect(self.save)
        self.button.move(0,100)
        self.show()

    def save(self):
        code = self.combo.currentText()
        #code = get_base_url(curr_val)
        print(code)
        new_table = get_page_content(Stock_Code)
        #new_table = get_page_content(code)
        #print(type(new_table))
        get_graphs(Stock_Code)
        #get_graphs(code)
        plt.show()


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
Stock_Code = 'NIFTY'

#Calling the get_graphs() to invoke graph generation
def get_graphs(Stock_Code):

    #Getting data content from the the selected code
    new_table=get_page_content(Stock_Code)

    # Reading the new_table into DataFrames to Segregate Calls, Puts and Strike Price Data
    call_df =pd.DataFrame(new_table.iloc[:,:10]).apply(pd.to_numeric)
    strike_price_df= pd.DataFrame(new_table.iloc[:,10]).apply(pd.to_numeric)
    put_df= pd.DataFrame(new_table.iloc[:,11:]).apply(pd.to_numeric)
    #print(call_df['OI'],type(put_df['OI']), type(strike_price_df))

    # Graph Params
    x_axis_index = np.array(strike_price_df['Strike Price'])
    bar_width = 30
    opacity = 0.8

    #Invoking the graphs
    get_graph_OI(call_df,put_df,x_axis_index=x_axis_index,bar_width=bar_width,opacity = opacity)
    get_graph_CHOI(call_df, put_df, x_axis_index=x_axis_index, bar_width=bar_width, opacity = opacity)

    #Enabling the cursor for hovering
    mplcursors.cursor(hover=True)
    # datacursor(hover =True)



# Function to generate graph for calls vs puts in OI
def get_graph_OI(call_df,put_df,x_axis_index,bar_width,opacity):
    #print("Im in OI")
    fig_1, ax_1 = plt.subplots()
    plot_calls_OI = plt.bar(x_axis_index,call_df['OI'], bar_width,
                     alpha=opacity,
                     color='green',
                     label='Calls')

    plot_puts_OI = plt.bar(x_axis_index + bar_width, put_df['OI'], bar_width,
                     alpha=opacity,
                     color='red',
                     label='Puts')

    plt.xlabel('Strike Price')
    plt.ylabel('Calls/Puts')
    plt.title( Stock_Code+ ' Calls vs Puts')
    #plt.xticks(x_axis_index, strike_price_df['Strike Price'], rotation=90, fontsize=6)
    plt.xticks(x_axis_index, rotation=90, fontsize=6)
    # Second Minimum Y axis
    call_df_OI_sort = sorted(set(call_df['OI']))
    put_df_OI_sort = sorted(set(put_df['OI']))
    y_axis_min_OI= min(call_df_OI_sort[1],put_df_OI_sort[1])
    # Maximum Y axis
    y_axis_max_OI = max(call_df['OI'].max(),put_df['OI'].max())
    plt.yticks(np.arange(y_axis_min_OI,y_axis_max_OI,step=150000), rotation=5,fontsize=6)
    plt.legend()
    plt.tight_layout()
    ani_1 = animation.FuncAnimation(fig_1, plot_calls_OI,plot_puts_OI, interval=100)


# Function to generate graph for calls vs puts in Change in OI
def get_graph_CHOI(call_df,put_df,x_axis_index,bar_width,opacity):
    #print("Im in cHNG OI")
    # create plot for change in OI in Calls vs Puts for every Strike Price
    fig_2, ax_2 = plt.subplots()
    plot_calls_chng_OI = plt.bar(x_axis_index,call_df['Chng in OI'], bar_width,
                     alpha=opacity,
                     color='blue',
                     label='Calls')

    plot_puts_chng_OI= plt.bar(x_axis_index + bar_width, put_df['Chng in OI'], bar_width,
                     alpha=opacity,
                     color='brown',
                     label='Puts')

    plt.xlabel('Strike Price')
    plt.ylabel('Calls/Puts Change In OI')
    plt.title(Stock_Code+ ' Calls vs Puts Change In OI')
    #plt.xticks(x_axis_index,strike_price_df['Strike Price'], rotation=90, fontsize=6)
    #print(plt.xticks(x_axis_index , strike_price_df['Strike Price'], rotation=90, fontsize= 6))
    plt.xticks(x_axis_index, rotation=90, fontsize=6)
    # Second Minimum Y axis
    call_df_CHOI_sort = sorted(set(call_df['Chng in OI']))
    put_df_CHOI_sort = sorted(set(put_df['Chng in OI']))
    y_axis_min_CHOI= min(call_df_CHOI_sort[1],put_df_CHOI_sort[1])
    # Maximum Y axis
    y_axis_max_CHOI = max(call_df['Chng in OI'].max(),put_df['Chng in OI'].max())
    plt.yticks(np.arange(y_axis_min_CHOI,y_axis_max_CHOI,step=75000),rotation=5 ,fontsize=6)
    #print(plt.yticks(np.arange(y_axis_min_CHOI,y_axis_max_CHOI,step=25000)))
    plt.legend()
    plt.tight_layout()

    ani_2 = animation.FuncAnimation(fig_2, plot_calls_chng_OI,plot_puts_chng_OI, interval=100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

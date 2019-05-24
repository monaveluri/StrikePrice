from Get_Quote_Data import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.animation as animation



#Fetching the Stock code from the drop down list defined
#Stock_Code = code
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

    '''x_axis_index = []
    for i,ind in enumerate(strike_price_df['Strike Price']):
        x_axis_index.append(ind)
    x_axis_index = np.array(x_axis_index)
    print(x_axis_index, type(x_axis_index))
    bar_width = x_axis_index*0.008'''

    '''x_axis_index = np.arange(len(strike_price_df))
    bar_width = 0.5
    opacity = 0.75'''

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
    plt.title('NIFTY 50 Calls vs Puts')
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
    plt.title('NIFTY 50 Calls vs Puts Change In OI')
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




'''cursor = Cursor(ax_2,
                    horizOn=True,
                    vertOn=True,
                    color='green',
                    linewidth= 2.0)
    def onclick(event):
        x1,y1 = event.xdata, event.ydata
        print(x1,y1)
    fig_2.canvas.mpl_connect('button_press_event', onclick)'''



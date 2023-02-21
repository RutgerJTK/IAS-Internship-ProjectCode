"""
Author: Rutger Kemperman
Goal of script: Plot the scraped data to check the correct data was scraped. (This checks out)
Future goal of script: Compare these trends data with data from NDFF or other biological databases. 
"""

import pandas as pd
import matplotlib.pyplot as plt

def parse_trends():
    trends_df = pd.read_csv("GTrendsTest1.csv")

    return trends_df

def plot_trends(trends_df):
    trends_df.plot(kind='line', x='date', y=['Blockchain', 'Cardano', 'Ethereum'])
    plt.title('Trends data for ' + trends_df.columns[1] + ", " + trends_df.columns[2] + " and " + trends_df.columns[3] + "over the past 5 years" )
    plt.ylabel('Relative popularity of search trend')
    plt.show()
    pass

if __name__ == "__main__":
    trends_df = parse_trends()
    plot_trends(trends_df)
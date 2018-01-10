import numpy as np
import pandas as pd
import datetime
import os

#define a conversion function for the native timestamps in the csv file
def dateparse (time_in_secs):
    a = datetime.datetime.fromtimestamp(float(time_in_secs))
    #only date is taken so as to make it easy to work on
    return a.date()

print('Using bitstampUSD_1-min_data...')
#Loading File will take some time
data = pd.read_csv('BTC_data.csv', parse_dates=True, date_parser=dateparse, index_col=[0])
data.head()

#Filling all the NA fields with zeros as no trading took place
data['Volume_(BTC)'].fillna(value=0, inplace=True)
data['Volume_(Currency)'].fillna(value=0, inplace=True)
data['Weighted_Price'].fillna(value=0, inplace=True)

#Filling below values with forward fill to as these values remain constant for the given time
data['Open'].fillna(method='ffill', inplace=True)
data['High'].fillna(method='ffill', inplace=True)
data['Low'].fillna(method='ffill', inplace=True)
data['Close'].fillna(method='ffill', inplace=True)

data.head()

#but we only need data from 2016-2017 so slicing the extracted data.
data = data.iloc[2099000:]
#Uncomment the line below to write the data on a csv
#data.to_csv('CleanedData.csv')

date_list =[data.iloc[i].name.date() for i in range(742377)]

uniq_dates = []
for i in date_list:
    if i not in uniq_dates:
        uniq_dates.append(i)

#getting the trading data of everyday's closing
data_c  = []
i = 0
for j in uniq_dates:
    try:
        while str(data.iloc[i].name.date()) == str(j):
            i+=1
        data_c.append(data.iloc[i-1])
    except:
        pass

#Writing into a dataframe
df = pd.DataFrame(data_c)

#list of all the closing values
clos_e = [df.iloc[i][3] for i in range(len(df))]


#Moving average algorithm
summ, moving_aves = [0], []
#N is the number of values of whose average one wants to take
N= 10
for i, x in enumerate(clos_e, 1):
    summ.append(summ[i-1] + x)
    if i>=N:
        moving_ave = (summ[i] - summ[i-N])/N
        moving_aves.append(moving_ave)

#Making dates array of same length as
dates = uniq_dates[:-1]
dates_1 = uniq_dates[:]
for i in range(len(uniq_dates)-len(moving_aves)):
    dates_1.pop(-1)

get_ipython().magic('pylab inline')
pylab.rcParams['figure.figsize'] = (14, 10)
plt.plot(dates,clos_e,label='Trading Graph')
plt.plot(dates_1,moving_aves,label='Moving averages')
plt.xlabel("Date")
plt.ylabel("Values")
plt.title("Moving Averages")
plt.legend()
plt.savefig("Moving.png")
plt.show()


#### Explanation

# >The Graph above is the result of implimentation of Moving average startegy for predicting the probable trend in the market, The Orange line gives you the head's up as to in which direction the market will move.
# >
# >**As we can see the part where the Orange line start's showing uptrend the market keeps going up, and starts moving down just before the market has a tendency to fall down or is going to change course.**

# I couldn't convert this line graph in a candle graph due to some issues else it would have been much clear as to at which intercection of the lines will the market show uptrend.
# We can also Implement _**fibonacci Retracement**_ to achieve a realtime trading ability i.e. to trade between the _**High's**_ and _**Low's**_.

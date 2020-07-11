try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2

from dateutil.relativedelta import relativedelta
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def pulldatagov (UID,dates=[]):
    '''
    Purpose:
    To use data from datagov website
    
    Function:
    If avaliable locally return cache
    else download from datagov.sg
    '''
    baseurl = "http://data.gov.sg/datastore/dump/"
    csvfile = UID
    urlcsv = baseurl + csvfile
    filename = "./data/" + csvfile + ".csv"
    
    if not os.path.isfile(filename):
        query = Request(urlcsv)
        query.add_header('User-agent', 'Mozilla/5.0')
        response = urlopen(query)
        #store query
        csv = urlopen(query).read().decode('UTF-8')
        # Write data to file
        file_ = open(filename, 'w')
        file_.write(csv)
        file_.close()

    #df = pd.read_csv(filename,index_col='_id', parse_dates=['month'], header=0)
    df = pd.read_csv(filename,index_col='_id', parse_dates=dates, header=0)
    
    return df

def pullquandl(UID):
    """
    Get Quandl Data
    """
    baseurl = "https://www.quandl.com/api/v3/datasets/ODA/"
    csvfile = UID
    urlcsv = baseurl + csvfile + '.csv?api_key=SES5ckjTYF1jR_TAQVZ9'
    filename = "./data/" + csvfile + ".csv"
    
    if not os.path.isfile(filename):
        query = Request(urlcsv)
        query.add_header('User-agent', 'Mozilla/5.0')
        response = urlopen(query)
        #store query
        csv = urlopen(query).read().decode('UTF-8')
        # Write data to file
        file_ = open(filename, 'w')
        file_.write(csv)
        file_.close()

    df = pd.read_csv(filename, parse_dates=['Date'], header=0)

    return df

def pullmasgov(UID):
    """
    Get MAS API Data , json
    """
    baseurl = "https://eservices.mas.gov.sg/api/action/datastore/search.json?limit=400&resource_id="
    csvfile = UID
    urlcsv = baseurl + csvfile
    filename = "./data/" + csvfile + ".csv"
    
    if not os.path.isfile(filename):
        query = Request(urlcsv)
        query.add_header('User-agent', 'Mozilla/5.0')
        response = urlopen(query)
        #store query
        csv = urlopen(query).read().decode('UTF-8')
        # Write data to file
        file_ = open(filename, 'w')
        file_.write(csv)
        file_.close()

    #df = pd.read_csv(filename, parse_dates=['Date'], header=0)

    return df



def plotexpdata(data,mthrange,noofruns,collectlistOfForcast,collectlistOfRuns,collectlistOfNumbers,countbelow,pct=True):
    """
    Streamline plotting function
    """
    
    dates_list = data.as_matrix(['month']).flatten()
    date_start = dates_list[0]
    date_end = dates_list[-1] + relativedelta(months=mthrange)

    listOfMonths = []

    
    #plt.xkcd()
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot2grid((6,4), (0,0))
    ax2 = plt.subplot2grid((6,4), (0,1))
    ax3 = plt.subplot2grid((6,4), (1,0), colspan=2, rowspan=2)

    #ax3.set_xlabel(("Year"),size=16)
    #ax3.set_ylabel(("Passenger Arrivals"),size=16)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, tick: str(int(x)/1000000)+'mil'))
    ax3.text(dates_list[50],3500000,('Actual Passenger Arrivals \n with ' + str(noofruns) + ' Monte Carlo Simulation Runs'),size=16)
    #ax.set_ylim(0,data.as_matrix(['no_of_air_passenger_arrivals']).max()*2)
    ax2.set_ylabel(("Arrival"),size=12)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, tick: str(int(x)/1000000)+'m'))
    ax2.tick_params(axis='x',labelsize=10)
    ax2.set_title(("Dist of simulated Arrivals at end of each run"),fontsize=10)
    #ax2.set_xlabel(("Runs"), va = 'top',size=12)
    ax.set_ylabel(("Frequency"),size=12)
    if pct:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, tick: str(int(x))+'%'))
    else:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, tick: str(int(x/1000))+'k'))
    ax.tick_params(axis='x',labelsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, tick: str(int(x)/1000)+'k'))
    ax.set_title(("M-o-M Growth Dist for simulated runs"),size=10)
    #ax.set_xlabel(("Simulated increase Mth-on-Mth"), va = 'top',size=12)

    x = mdates.date2num(dates_list)
    y = data.as_matrix(['no_of_air_passenger_arrivals']).flatten()

    z=np.polyfit(x,y,2)
    p=np.poly1d(z)

    x2 = np.append(x,mdates.date2num(date_end))
    y2 = p(x2)

    # Plot line and area below
    ax2.plot(range(noofruns),np.sort(collectlistOfForcast),color='k')
    ax2.fill_between(range(noofruns),np.sort(collectlistOfForcast),collectlistOfForcast.min(),color='g')
    #plot Montecarlo Runs
    for x in range (0,mthrange):
        listOfMonths.append(dates_list[-1] + relativedelta(months=x))
    for run in collectlistOfRuns:
        ax3.plot_date(np.array(listOfMonths),np.array(run),'g-',alpha=0.3)
    # Actual Data graph
    ax3.plot_date(data['month'],y,fmt='-',label = "Actual")
    ax3.plot(x2,y2,'r--', label = "Trend")
    # Last Actual Arrival
    ax2.plot((0, noofruns), (y2[-1], y2[-1]), 'r--')
    ax2.text(noofruns/10 , y2[-1] + 500000, ('Forecast at yr ' + str(date_end.year)),size=10,color='r')
    ax2.text(noofruns/10 ,1000000,(str(countbelow) + ' Runs are below prediction'),size=12,color='k')
    # Histogram of Growth percentage
    ax.hist(collectlistOfNumbers)
    ax3.legend(loc='lower right',fontsize=12)
    plt.show()
    
    fig.clf()
    plt.clf()
#dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup


#home dates for Miami Dolphins games in the past two seasons
home_dates=['2017-10-01', '2017-10-08', '2017-10-22', '2017-11-05', '2017-11-19', '2017-12-03','2017-12-11','2017-12-31', \
             '2018-9-09', '2018-9-23', '2018-10-14', '2018-10-21', '2018-11-04', '2018-12-02','2018-12-09','2018-12-23']

#away dates for Dolphins games in the past two seasons
away_dates=['2017-9-17','2017-9-24','2018-9-16', '2017-10-15', '2017-10-26', '2017-11-13', '2017-11-26','2018-9-30',\
              '2017-12-17', '2018-12-30', '2017-12-24', '2018-10-07', '2018-10-25', '2018-11-11','2018-11-25','2018-12-16' ]

#wunder ground urls for locations and dates for away games in the past two seasons
away_game_url = ['https://www.wunderground.com/history/daily/us/ca/san-diego/date/2017-9-17',\
                'https://www.wunderground.com/history/daily/us/nj/east-rutherford/date/2017-9-24',\
                'https://www.wunderground.com/history/daily/us/nj/east-rutherford/date/2018-9-16',\
                'https://www.wunderground.com/history/daily/us/ga/atlanta/date/2017-10-15',\
                'https://www.wunderground.com/history/daily/us/md/baltimore/date/2017-10-26',\
                'https://www.wunderground.com/history/daily/us/nc/charlotte/date/2017-11-13',\
                'https://www.wunderground.com/history/daily/us/ma/foxborough/date/2017-11-26',\
                'https://www.wunderground.com/history/daily/us/ma/foxborough/date/2018-9-30',\
                'https://www.wunderground.com/history/daily/us/ny/buffalo/date/2017-12-17',\
                'https://www.wunderground.com/history/daily/us/ny/buffalo/date/2018-12-30',\
                'https://www.wunderground.com/history/daily/us/mo/kansas-city/date/2017-12-24',\
                'https://www.wunderground.com/history/daily/us/oh/cincinnati/date/2018-10-07',\
                'https://www.wunderground.com/history/daily/us/tx/houston/date/2018-10-25',\
                'https://www.wunderground.com/history/daily/us/wi/green-bay/date/2018-11-11',\
                'https://www.wunderground.com/history/daily/us/in/indianapolis/date/2018-11-25',\
                'https://www.wunderground.com/history/daily/us/mn/minneapolis/KMSP/date/2018-12-16']

#Lists that will allow the script to continue even if the scrape errors
backup_home_avg_list = [86,87,84,77,73,74,58,62,83,83,83,83,82,80,78,63]
backup_away = [72,78,76,74,51,53,44,62,22,30,21,77,65,29,49,39]

#Dictionary with information about games in the past two seasons
dates = {"Dates": ['2017-9-17', '2017-9-24','2017-10-01', '2017-10-08',\
                    '2017-10-15', '2017-10-22', '2017-10-26', '2017-11-05',\
                  '2017-11-13', '2017-11-19', '2017-11-26', '2017-12-03',\
                  '2017-12-11', '2017-12-17', '2017-12-24', '2017-12-31',\
                   '2018-9-09', '2018-9-16','2018-9-23', '2018-9-30', \
                   '2018-10-07','2018-10-14', '2018-10-21', '2018-10-25', \
                   '2018-11-04', '2018-11-11','2018-11-25','2018-12-02',\
                   '2018-12-09', '2018-12-16', '2018-12-23', '2018-12-30'],
        'Location': ['Away_San Diego', 'Away_New York', 'Home', 'Home', \
                     'Away_Atlanta', 'Home', 'Away_Baltimore','Home',\
                     'Away_Carolina', 'Home', 'Away_New England','Home',\
                     'Home', 'Away_Buffalo', 'Away_Kansas City','Home',\
                    'Home', 'Away_New Jersey', 'Home', 'Away_New England',\
                     'Away_Cincinatti','Home', 'Home','Away_Texans', \
                     'Home', 'Away_Green Bay', 'Away_Indy','Home',\
                     'Home', 'Away_Minn', 'Home', 'Away_Buffalo'],
        'Opponent': ['Chargers', 'Jets', 'Saints','Titans', 'Falcons', 'Jets','Ravens','Raiders',\
                    'Panthers','Buccaneers','Patriots','Broncos','Patriots','Bills','Chiefs','Bills',\
                    'Titans','Jets','Raiders','Patriots','Bengals','Bears','Lions','Texans',\
                    'Jets','Packers','Colts','Bills','Patriots','Vikings','Jaguars','Bills'],
        'Result':['Win','Loss','Loss','Win','Win', 'Win','Loss','Loss',\
                 'Loss','Loss','Loss','Win','Win','Loss','Loss','Loss',\
                 'Win','Win','Win','Loss','Loss','Win','Loss','Loss',\
                 'Win','Loss','Loss','Win','Win','Loss','Loss','Loss'],
        'Score':['19-17','20-6','20-0','16-10','20-17','31-28','40-0','27-24',\
                '45-21','30-20','35-17','35-9','27-20','24-16','29-13','22-16',\
                '27-20','20-12','28-20','38-7','27-17','31-28','32-21','42-23',\
                '13-6','31-12','27-24','21-17','34-33','41-17','17-7','42-17']}


#converting the dictionary to a dataframe
data = pd.DataFrame(data = dates)



def get_home_urls():
    """Generates urls for home games"""
    url = 'https://www.wunderground.com/history/daily/us/fl/fort-lauderdale/KFLL/date/' #wunder ground url
    home_game_url = []                                                                  #empty list urls will be appended into
    for date in home_dates:                                                             #loop through the home_dates list to create the urls
        gameday_url = url + date
        home_game_url.append(gameday_url)
    return home_game_url                                                                # return a list of home game urls




def home_temp_scrape(url_list):
    """Scrapes wunderground selecting the daily average temperature for Home Games at HardRock Stadium."""
    avg_temp_list = []                                          #list that values will be appended into
    for url in url_list:                                        #loops through urls to parse
        page = requests.get(url).text                           #get html from page
        soup = BeautifulSoup(page, 'html.parser')               #creats beautiful soup object
        try:                                                    #Often errors due to Index Error and site security, allows script to continue to run
            avg_temp = soup.find_all('tr')[3].find('td').text   #navigation to avg temperature for that day
            avg_temp_list.append(avg_temp)                      #inserts the value into the list
        except: IndexError                                      #Error that occurs

    return avg_temp_list  


def away_game_scrape(url_list):
    """Scrapes wunderground selecting the average daily temperature for various away game locations on gamedays."""
    away_avg_temp_list=[]                                        #list that values will be appended into
    for url in url_list:                                         #loops through urls to parse
        page = requests.get(url).text                            #get html from page
        soup = BeautifulSoup(page, 'html.parser')                #creatse beautiful soup object
        try:                                                     #Often errors due to Index Error and site security, allows script to continue to run
            avg_temp = soup.find_all('tr')[3].find('td').text    #navigation to avg temperature for that day
            away_avg_temp_list.append(avg_temp)                  #inserts the value into the list
        except: IndexError                                       #Error that occurs
    return away_avg_temp_list


def eval_scrapes(home_weather, away_weather):
    """Evaluates whether the scrapes returned a full set of temperatures"""
    if len(home_weather) <16:                       #Checks to see if list contains values for all dates
        home_weather = backup_home_avg_list         #If scrape did not get all values, utilizes backups
    if len(away_weather) < 16:
        away_weather = backup_away
    return home_weather, away_weather

def temp_to_dataframe(home_date, home_weather, away_date, away_weather ,dataframe):
    """Adding the scraped temperatures to the dataframe"""
    home_dict = dict(zip(home_date,home_weather))                    #Converts the home game dates and weather to a dictionary
    away_dict = dict(zip(away_date,away_weather))                    #Converts the away game dates and weather to a dictionary

    home_dict.update(away_dict)                                     #Mergeres dictionaries together
    dataframe['Temperature(°F)'] = dataframe['Dates'].map(home_dict)    #Adds temperatures to dataframe column

    return dataframe

def has_dome():
    """Creates dataframe column indicating whether a team plays in a dome"""
    plays_in_dome = ['Away_Atlanta','Away_Indy', 'Away_Minn', 'Away_Texans']  #Teams that play in domes
    data['Dome']= data.Location.isin(plays_in_dome)                            #Creates dataframe column with True representing that a team plays in a dome
    return data





home_game_url = get_home_urls()                                                          #Calls function to create home game urls

home_temperatures = home_temp_scrape(home_game_url)                                     #Scrapes home game temperatures

away_temperatures = away_game_scrape(away_game_url)                                      #Scrapes away game temperatures

home_temperature, away_temperature = eval_scrapes(home_temperatures, away_temperatures)   #Determine if scrape was successfull and if not use backup data 

data = temp_to_dataframe(home_dates,home_temperature,away_dates,away_temperature, data)    #Input the temperature results to the dataframe 

data = has_dome()                                                                           #Creates column where games were played in domes


print(data)


#Creating PDf Copy of Report


import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table

ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, data, loc='center')

plt.savefig('./data_table.jpg',  bbox_inches='tight', dpi=400)

#Lay out for the PDF
from fpdf import FPDF, HTMLMixin
 
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=22)
pdf.cell(w=200, h= 15, txt="Miami Dolphins Weather Report", ln=1, align="C")
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt='Created by Nicholas Radich', ln=2,align= 'C')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt='Data acquired from www.wunderground.com', ln=3,align= 'C')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt='Findings of Weather Analysis:', ln=4,align= 'L')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt="The average temperature of Dolphins game over the past two years was 64°F.", ln=4,align= 'L')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt="The low temperature of Dolphins game over the past two years was 21°F.", ln=4,align= 'L')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt="The high temperature of Dolphins game over the past two years was 87°F.", ln=4,align= 'L')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt="The average temperature in Dolphins victories was 78°F.", ln=4,align= 'L')
pdf.set_font('Arial', size =14)
pdf.cell(w=200, h=10, txt="The average temperature in Dolphins home games was 77.25°F.", ln=4,align= 'L')
pdf.image('data_table.jpg',x =25, y=105,w=150, h=175)
pdf.output("Dolphins_Weather_Report.pdf")
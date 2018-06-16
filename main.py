#importing all the required libraries
import requests
import json
import datetime
import pymongo
import time
import threading
import matplotlib.pyplot as plt
import webbrowser
from matplotlib.dates import DateFormatter

#Connecting to the MongoDb Database
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.weather  #Created a database called weather in mongodb
collection = db.forecast  # Created a collection called'forecast' in mongodb

def locations():
   #3a and 3b:Locations to be monitored are placed in the configuration file, refresh frequency is given in that file.
   #retieving the locations from the config file.
    data = json.load(open('configuration_file.json'))
    return data

#Requesting the weather data and converting it to a json object for one request	
def weather_forecast(city_id, api_key):
    url_to_process = "http://api.openweathermap.org/data/2.5/forecast?id=" + city_id + "&appid=" + api_key
    response = requests.get(url_to_process)
    return response.json()
	
# created a function to convert from kelvin to fahrenheit
def kelvin_to_fahrenheit(kelvins):
    return ((9/5) * (kelvins - 273)) + 32
	
# 4.creating a function for 5days/3hour forecast
def five_day_forecast():
    while True:
        print ('5 days/3 hour Forecast Thread')

        data = locations()
        api_key = data['api']
        cities = data['cities']
        refresh_rate = data['refresh_rate']

        for city in cities:
            print ("Processing ") + str(city['name']) + str(city['country']) + (" to get data and saving to database")
            json_object = weather_forecast(str(city['id']), api_key)
            status = data_store_db(json_object)
            #print status
        time.sleep(refresh_rate)
		
# 5. creating a function for 16 days/daily forecast
def sixteen_days_forecast():
   
        #similar to the above function but i was
        #Not able to do this because we need a paid subscription to do this.
        pass
		
# 6. Created a function for the weather maps
def weather_maps():
    Browser_flag = True
    while True:
        print ('Weather map layers to show temperature layer in a windowed or browser')

        # TODO
        # Code for downloading weather maps layers every 60 seconds
        #It can be implemented using own customized libraries in future
        #Meanwhile, using JavaScript and Browser to show temperature layer on maps

        #Opening browser only once
        if Browser_flag:
            print ("Opening web browser and displaying the latest temperature layer on the world map")
            webbrowser.open_new('weather_map.html')
        time.sleep(60)
        Browser_flag = False
		
# 7. Storing data in the mongodb database
def data_store_db(json_object):
    
    cnt = json_object['cnt']
    city_name = json_object['city']['name']
    city_id = json_object['city']['id']
    country = json_object['city']['country']

    for i in range(cnt):
        dt, required_data = data_process(json_object['list'][i])
        alerts(city_name, country, required_data)
        #print dt, required_data
        collection.update_one(
			{"dt": dt,
			 'city_id': city_id,
			 'city_name': city_name,
			 'country': country},
			{
				"$set": required_data
			},
			True
		)

    return True
	
# 8. Created a function to open the weather map in a new window
def open_and_display_graph():
    while True:
        #If data is not available, it'll try again after 1 minute
        try:
            print ('Getting the 10 forecast data and showing the graph for temperatures')
            data = locations()
            cities = data['cities']
            for city in cities:
                cursor = collection.find({'city_id': city['id']}).sort([("dt_txt", -1)]).limit(80);  
                dt_data = []
                temperature_data = []
                for document in cursor:
                    dt_data.append(document['dt_txt'])
                    temperature_data.append(document['main']['temp'])
                    #print document['city_name'] + ": " + str(document['main']['temp'])
                plot_temperature_data(document['city_name'], dt_data, temperature_data)

            time.sleep(90)
        except:
            time.sleep(60)
			
# 9. Created alerts function to print out alerts if there is rain/snow. 
def alerts(city_name, country, required_data):
    temp = required_data['main']['temp']
    condition = (required_data['weather'][0]['main']).lower()
    timestamp = required_data['dt_txt']
    #print timestamp, temp, condition

    if temp < 2:
        print ("ALERT")
        print ("Freezing temperature of " + str(temp) + " in the " + str(city_name) + ", " + str(country) + " around " + str(timestamp))

    if condition.find('rain') >= 0 or condition.find('snow') >= 0:
        print (" WEATHER   ALERT")
        print ("Its going to " + condition + " in " + str(city_name) + ", " + str(country) + " around " + str(timestamp))


#Filtering Data for converitng datetime stamp to date format and massaging rest of it for avoiding duplicate entries in the database		
def data_process(dataset):
    processed_dictionary = dataset
    processed_dictionary['dt_txt'] = datetime.datetime.strptime(dataset['dt_txt'], '%Y-%m-%d %H:%M:%S')
    processed_dictionary['main']['temp'] = kelvin_to_fahrenheit(dataset['main']['temp'])
    dt = dataset['dt']
    try:
        del processed_dictionary['dt']
    except Exception as e:
        return False
    return dt, processed_dictionary
	
# created a function to run all the threads
def controller():

    print ("Application is Started")
    #Creating threads for all the tasks
    five_day_forecast_thread = threading.Thread(target = five_day_forecast)
    sixteen_days_forecast_thread = threading.Thread(target = sixteen_days_forecast)
    weather_maps_thread = threading.Thread(target = weather_maps)
    open_and_display_maps_thread = threading.Thread(target = open_and_display_graph)

    #Running the threads
    five_day_forecast_thread.start()
    sixteen_days_forecast_thread.start()
    weather_maps_thread.start()
    open_and_display_maps_thread.start()
	
if __name__ == '__main__':
    try:
        controller()
    except Exception as e:
        print ('Error Running the code : ') 
        exit()
    except KeyboardInterrupt:
        exit()

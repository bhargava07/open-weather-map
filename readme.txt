Python based multi-strung application that can download the climate figure from the open climate guide and store the information 
in archive shape in the NoSQL database(MongoDB)

steps to follow:

1.First, Install all the required libraries. the required libraries are:
    1-threading
    2-json
    3-datetime
    4-webbrowser
    5-time
    6-requests
    7-matplotlib
    8-pymongo
 All the required libraries can be installed using pip install library name
 
2-Start mongodb server on your gadget locally or remotely and change accreditations as needs be in the code. In the event that need 
assistance installing mongodb, take after guideline here as per your OS: 
https://docs.mongodb.com/manual/organization/introduce network/ 

3.3-Create Database named 'weather' or your own particular database name however keep in mind to rename it in the code 

4.Create Collection named 'forecast' in the weather database. 

5.Create an account in the 'https://openweathermap.org/' to get the API access key.

6.Create a configuration file, place all the locations which has to be monitored in that file.put a refresh frequency in that file.

7.The API key must be mentioned in the configuration file, main python file and the weather_map.html file.

8.The main.py file code has been explained in that file using comments.

9.Run the code.







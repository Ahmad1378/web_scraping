import re
import bs4
import requests
import mysql.connector

input = str(input("Enter your desired car brand and model (like peugeot/pars or bmw/x5)."))

link = "https://bama.ir/car/" + input

r = requests.get (link)

soup = bs4.BeautifulSoup( r.text , "html.parser" )

cars = soup.find_all('div' , attrs = {'class' : 'listdata'})

cars_price = []
cars_function = []

for car in cars :

    cars_price.append ( re.sub ( r'\s+' , ' ' , car.find('p' , attrs = {'class' : 'cost'}).text).strip())
    cars_function.append ( re.sub (r'\s+' , ' ' , car.find('p' , attrs = {'class' : 'price hidden-xs'}).text).strip())
     

cnx = mysql.connector.connect( user = 'root' , password = '' ,
                                     host = '127.0.0.1' , database = 'mydatabase' )
                                     
cursor = cnx.cursor()

i = 0

for i in range (len(cars_function)):
    if i >= 20 :
        break
    query = "INSERT INTO cars VALUES (%s , %s)"
    values = (cars_function[i] , cars_price[i])
    cursor.execute(query,values)
    cnx.commit()
    
cnx.close()

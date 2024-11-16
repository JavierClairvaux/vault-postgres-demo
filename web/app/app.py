# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request 
import psycopg2
import json

# creating a Flask app 
app = Flask(__name__) 
f = open('/app/creds.json')
credentials = json.load(f)
f.close()

def getData(database, user, password):
    conn = psycopg2.connect(database = database, 
                        user = user, 
                        host= 'sampledb',
                        password = password,
                        port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM datacamp_courses;')
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/', methods = ['GET', 'POST']) 
def home(): 
    if(request.method == 'GET'): 
  
        data = getData("postgres", credentials['username'], credentials['password'])
        return data
  
  

if __name__ == '__main__': 
  
    app.run(host='0.0.0.0', debug = True)
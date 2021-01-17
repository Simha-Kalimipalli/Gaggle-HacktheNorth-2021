from flask import Flask, render_template, request, redirect, url_for
#from flask import jsonify

# data science related
import csv
import pandasql as ps
import json
import pandas as pd
import numpy as np

app = Flask(__name__)

"""
@app.route('/')

def index():
    # return "hi"
    return render_template('home.html')
    
    """

@app.route('/')

def index():
   # return "hi"
    return render_template('index.html')

@app.route('/searchbar',  methods=['GET','POST'])
def searchbar():
    if request.method == "POST":
        search = request.form['search']
        locasearch = request.form['locasearch']

        #print(search)
        #print(locasearch)

        # Step 1:  Read a CSV file into DataFrame (A Dataframe is a table)
        event_data = pd.read_csv('eventlist.csv', sep=',', engine='python')
        print(event_data)

        j_sql = """select * from event_data where tag like '%"""  + search + """%' and location like '%""" + locasearch +"""%'"""

        fin_data = ps.sqldf(j_sql, locals())
        print(fin_data)
        fin_data.to_csv('findata.csv')

        with open('findata.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            first_line = True
            events = []
            for row in data:
              if not first_line:
                events.append({
                  "eventname": row[1],
                  "eventdate": row[2],
                  "eventtime": row[3],
                  "description": row[4],
                   "location": row[5],
                    "latitude": row[6],
                    "longitude": row[7],
                    "numguests": row[8],
                    "link": row[9],
                    "picturelink":row[10]

                })
              else:
                first_line = False

     #return "hello"
        return render_template('events.html', events=events, search=search, locasearch=locasearch)
    else:
        return redirect(url_for('index'))

@app.route('/add')
def addfunc():

     #return "hi"
    return render_template('home.html')


@app.route('/your-url', methods=['GET','POST'])

def your_url():
    if request.method == "POST":

        eventname = request.form['eventname']
        eventdate = request.form['eventdate']
        eventtime = request.form['eventtime']
        description = request.form['description']
        location = request.form['location']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
       # picture = request.form['picture']
        numguests = request.form['numguests']
        urlevent = request.form['urlevent']
        urlpicture = request.form['urlpicture']
        tag = request.form['tag']

        fieldnames =['eventname', 'eventdate', 'eventtime', 'description', 'location', 'latitude','longitude', 'numguests', 'urlevent', 'urlpicture',  'tag']
        with open('eventlist.csv','a', newline='') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames)
            writer.writerow({'eventname':eventname,'eventdate':eventdate, 'eventtime':eventtime, 'description':description , 'location':location, 'latitude':latitude, 'longitude':longitude, 'numguests':numguests, 'urlevent':urlevent, 'urlpicture':urlpicture, 'tag':tag })

        return render_template('your_url.html')
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
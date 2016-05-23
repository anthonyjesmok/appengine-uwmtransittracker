# Imports
import os
import jinja2
import json
import logging
import urllib2
import datetime
import xml.etree.ElementTree as etree
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import timedelta

###INSERT YOUR MCTS BUSTIME API KEY BELOW###
mctsKey = ""
###INSERT YOUR MCTS BUSTIME API KEY ABOVE###

# Shared Functions
def parseStops():
    load_data = urllib2.urlopen("https://raw.githubusercontent.com/anthonyjesmok/appengine-uwmtransittracker-stopsjson/master/stops.json")
    json_data = load_data.read()
    data = json.loads(json_data)
    return data["stops"]

def getUWMPredictions(stop):
    times = []
    xmlFeed = urllib2.urlopen('http://webservices.nextbus.com/s/xmlFeed?command=predictions&a=uw-mil&stopId=' + stop)
    tree = etree.parse(xmlFeed)
    root = tree.getroot()
    for child in root:
            for direction in child:
                for pred in direction:
                    toPush = {
                                'system': "University of Wisconsin-Milwaukee Parking & Transit",
                                'route': str(child.attrib['routeTitle']) + " " + str(direction.attrib['title']).title(),
                                'minutes': int(pred.attrib['minutes']),
                                'stop_name': str(child.attrib['stopTitle']),
                                'stop_num': stop
                                }
                    times.append(toPush)
    logging.info(times)
    return times

def getMCTSPredictions(stops):
    times = []
    stops_csv = ','.join(map(str, stops))
    xmlFeed = urllib2.urlopen('http://realtime.ridemcts.com/bustime/api/v1/getpredictions?key=' + mctsKey + '&stpid=' + stops_csv)
    tree = etree.parse(xmlFeed)
    root = tree.getroot()
    # Subtract 6 Hours for Central TIme
    now = datetime.datetime.now() - timedelta(hours=5)
    for child in root:
        time_diff = datetime.datetime.strptime(child[10].text, "%Y%m%d %H:%M") - now
        minutes = int(time_diff.total_seconds() / 60)
        if str(child[6].text) == "GOL":
            child[6].text = "GoldLine"
        toPush = {
                  'system': "Milwaukee County Transit System",
                  'route':  str(child[6].text) + " " + str(child[8].text).title() + " to " + str(child[9].text),
                  'minutes': int(minutes),
                  'stop_name': str(child[2].text).title(),
                  'stop_num': int(child[3].text)
                  }
        times.append(toPush)
    logging.info(times)
    return times

# Handler Classes
class MainHandler(webapp.RequestHandler):
    def get(self):
        stops = parseStops()
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render({'stops': stops}))

class StopHandler(webapp.RequestHandler):
    def get(self):
        requested_stop = self.request.get('id')
        stops = parseStops()
        raw_times = []
        times = []
        for stop in stops:
            if stop['uwm_tag'] == requested_stop:
                raw_times = getUWMPredictions(stop['uwm_id']) + getMCTSPredictions(stop['mcts'])
                break
        raw_times = sorted(raw_times, key=lambda k: k['minutes'])
        for idx in range(len(raw_times)):
            if idx > 0 and raw_times[idx-1]['minutes'] != raw_times[idx]['minutes'] and raw_times[idx-1]['route'] != raw_times[idx]['route']:
                times.append(raw_times[idx])
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render({'stops': stops, 'times': times}))
        
# Bootstrap
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname('_file_'), '')))
application = webapp.WSGIApplication([('/', MainHandler), ('/stop', StopHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

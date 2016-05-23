Important Note: Recently, the University of Wisconsin-Milwaukee discontinued their API for real-time shuttle tracking pending a complete renovation of the shuttle service. As a result, this project is no longer functional. This code will remain up on GitHub for viewing and critique, but the live site has been taken down.
-----------

UWM Transit Tracker
===========================
I built this tool out of frustrations that myself and other students were having with our University's shuttle system. Many students started to take MCTS buses to and from campus instead of the shuttles, but could never make a sound decision which bus or shuttle to wait for or which stop to stand at. This can be a problem, especially in cold Wisconsin winters.

Using real-time data from both systems, this tool displays arrival times for both the University of Wisconsin-Milwaukee (UWM) shuttle stops and Milwaukee County Transit System (MCTS) bus stops serving the UWM area.

Technologies Used
-----------------
 - [Materialize.css](http://materializecss.com/ "Materialize.css")
 - [Google App Engine](https://cloud.google.com/appengine/ "App Engine")
 - [Jinja2](http://jinja.pocoo.org/ "Jinja2")

APIs Used
---------
 - [MCTS BusTime API](http://realtime.ridemcts.com/bustime/createAccount.jsp "BusTime")
	 - If you want to test this application in your own development environment, you will need to register for a key and place it where stated in main.py.
 - [NextBus API](http://api-portal.anypoint.mulesoft.com/nextbus/api/nextbus-api "NextBus API")
	 - The base URL is a bit different since UWM's feed is not listed on the public directory, but the API methods are the same as in these docs. 

Stops.json
-------
You probably are wondering what that stops.json file contains. First of all, it has to be loaded remotely since App Engine does not like static text-based files too much. Second, that file is hosted in the repo [appengine-uwmtransittracker-stopsjson](https://github.com/anthonyjesmok/appengine-uwmtransittracker-stopsjson "appengine-uwmtransittracker-stopsjson"). You can take a look and contribute if you would like!
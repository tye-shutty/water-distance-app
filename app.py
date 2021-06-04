#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session, send_file, send_from_directory, render_template
from flask_restful import Resource, Api, reqparse
import settings
import requests
import csv, sys
from datetime import datetime
import ssl

app = Flask(__name__, static_folder="build/static", template_folder="build")
app.secret_key = settings.SECRET_KEY

# class Root(Resource):
#   def get(self):
#     # return send_file(filename_or_fp=settings.STATIC_FOLDER+'/index.html') 
#     # return app.send_static_file('index.html')
#     # return send_from_directory(app.static_folder, 'index.html')
#     # return render_template('index.html')
#     # response = make_response(render_template('test.html'))
#     # response.headers['content-type'] = 'text/html'
#     # return response
#     return send_file('build/test.html')

class History(Resource):
  def get(self):
    with open('to_Elsys_sensor_data.csv') as csv_file:
      courses_input = csv.reader(csv_file, delimiter=',')
      sensors = dict()
      time_labels = []
      valid_sensors = set(["a81758fffe059fdd", "a81758fffe059fdc", 'a81758fffe03e451']) 
      for (_, my_id, _, _, _, distance, _, time) in list(courses_input)[1:]:
        if my_id in valid_sensors :
          if(my_id not in sensors):
            sensors[my_id] = []
          try:
            dt = datetime.strptime(time, '%Y/%m/%d %H:%M:%S.%f+00')
          except:
            dt = datetime.strptime(time, '%Y/%m/%d %H:%M:%S+00')
          time_num = dt.timestamp()
          sensors[my_id].append({'x': time, 'y': distance})
          if(len(time_labels) == 0 or time_labels[-1] != time):
            time_labels.append(time)

      sensors['time_labels'] = time_labels
    return make_response(jsonify(sensors), 200)

class Current(Resource):
  def get(self):
    data = requests.get('https://opendata.arcgis.com/datasets/b7e729a865b142dfaa379a00b3dc70d6_0.geojson')
    data = data.json() #decodes json
    levels = {}
    # print(data)
    for f in data['features']:
      levels[f['properties']['DevEUI']] = f['properties']['Distance']

    return make_response(jsonify(levels), 200)
    # with open('to_Elsys_sensor_data.csv') as csv_file:
    #   courses_input = csv.reader(csv_file, delimiter=',')
    #   sensors = dict()
    #   time_labels = []
    #   valid_sensors = set(["a81758fffe059fdd", "a81758fffe059fdc", 'a81758fffe03e451']) 
    #   for (_, my_id, _, _, _, distance, _, time) in list(courses_input)[1:]:
    #     if my_id in valid_sensors :
    #       if(my_id not in sensors):
    #         sensors[my_id] = []
    #       try:
    #         dt = datetime.strptime(time, '%Y/%m/%d %H:%M:%S.%f+00')
    #       except:
    #         dt = datetime.strptime(time, '%Y/%m/%d %H:%M:%S+00')
    #       time_num = dt.timestamp()
    #       sensors[my_id].append({'x': time, 'y': distance})
    #       if(len(time_labels) == 0 or time_labels[-1] != time):
    #         time_labels.append(time)

    #   sensors['time_labels'] = time_labels
    # return make_response(jsonify(sensors), 200)
api = Api(app)

root = '/water/sensors'
# api.add_resource(Root, root)
api.add_resource(History, root+'/history')
api.add_resource(Current, root+'/current')

if __name__ == "__main__":

  if(settings.APP_HOST != 'tyeshutty.tk'):
    context = ('cert.pem', 'key.pem')
    app.run(host=settings.APP_HOST, 
      port=settings.APP_PORT, 
      ssl_context=context,
      debug=settings.APP_DEBUG)
  else:
    app.run(debug=settings.APP_DEBUG)

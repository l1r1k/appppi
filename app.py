import pathlib
import json
import os
import parser_1
from flask import Flask
from flask_restful import Api, Resource, reqparse

parser = parser_1


app = Flask(__name__)
api = Api(app)
      


class Quote(Resource):
    def get(self,id='0'):
        parser.click()
        read_groups = pathlib.Path(os.path.abspath("info.json")).read_text(encoding="utf-8")

        groups = json.loads(read_groups)
        if id == '0':
            return groups, 200
        for quote in groups:
            if(quote['id'] == id):
                return quote, 200
        return "Quote not found", 404
    
class Schedule(Resource):
    def get(self,id='0'):
        parser.click()
        read_schedule = pathlib.Path(os.path.abspath("schedule.json")).read_text(encoding="utf-8")

        schedule = json.loads(read_schedule)
        if id == '0':
            return schedule, 200
        for quote in schedule:
            if(quote['id'] == id):
                return quote, 200
        return "Quote not found", 404
    
class ChangedSchedule(Resource):
    def get(self,id='0'):
        parser.click()
        read_changed_schedule = pathlib.Path(os.path.abspath("changedschedule.json")).read_text(encoding="utf-8")

        changed_schedule = json.loads(read_changed_schedule)
        if id == '0':
            return changed_schedule, 200
        for quote in changed_schedule:
            if (id in quote['dicts']):
                return quote['dicts'].get(id), 200
        return "Quote not found", 404
    
class Week(Resource):
    def get(self,id='Неделя'):
        parser.click()
        read_week = pathlib.Path(os.path.abspath("week.json")).read_text(encoding="utf-8")

        week = json.loads(read_week)
        if id == 'Неделя':
            return week, 200
        return "Quote not found", 404
    
class Time(Resource):
    def get(self,id='0'):
        parser.click()
        read_time = pathlib.Path(os.path.abspath("timeschedule.json")).read_text(encoding="utf-8")

        time = json.loads(read_time)
        if id == '0':
            return time, 200
        for quote in time:
            if(quote['id'] == id):
                return quote, 200
        return "Quote not found", 404   

    
api.add_resource(Quote, "/groups", "/groups/", "/groups/<string:id>")
api.add_resource(Schedule, "/schedule", "/schedule/", "/schedule/<string:id>")
api.add_resource(ChangedSchedule, "/changed_schedule", "/changed_schedule/", "/changed_schedule/<string:id>")
api.add_resource(Week, "/Week", "/Week/", "/Week/<string:id>")
api.add_resource(Time, "/time", "/Time/", "/Time/<string:id>")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
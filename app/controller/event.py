from flask import request, Blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from ..model.Events import Event
import requests
from ..constants import TRAINING_START, APP_LAUNCH, TRAINING_FINISH, NOTIFY_MICROSERVICE_URL, ALLOWED_EVENTS, DATE_FORMAT
from datetime import datetime
from ..utils.exceptionHandler import serviceUnavailable

scheduler = BackgroundScheduler()
scheduler.start()

event = Blueprint('event', __name__)

cache = {}

def notifyOnInactivity():
    currentTime = datetime.now()
    currentTime = currentTime.strftime(DATE_FORMAT)
    currentTime = datetime.strptime(currentTime, DATE_FORMAT)
    removeKeys = []

    if(len(cache)>0):
        for key in cache.keys():
            if(cache[key].getType() == APP_LAUNCH and ((currentTime - cache[key].getTimestamp()).total_seconds()/60)>10):
                msg= f"Hi {key}! You have been inactive for more than 10 mins. Please start the training" 
                print(msg)
                removeKeys.append(key)
                # api call to /v1/notify 
                try:
                    message_data = {'message': msg}
                    notify = requests.post(NOTIFY_MICROSERVICE_URL + '/v1/notify' , json=message_data)
                except:
                    serviceUnavailable("notification")
        list(map(cache.pop, removeKeys))
                

# frequency of job can be changed based on requirements.
scheduler.add_job(notifyOnInactivity, 'interval', minutes=1)


@event.route('/', methods=["POST"])
def processEvents():
    eventData = request.get_json()
    newEvent = Event(eventData.get("user_id"), eventData.get("type"), eventData.get("time_stamp"), eventData.get("training_program_id"))
    if(eventData.get("type") in ALLOWED_EVENTS):
        if(newEvent.userId in cache.keys() and cache[newEvent.userId].getType() == TRAINING_START and newEvent.type == TRAINING_FINISH):
            timeSpent = (newEvent.timestamp - cache[newEvent.userId].getTimestamp()).total_seconds()/60
            if(timeSpent >30):
                msg= f"Congratulations {newEvent.userId}! on successsfully completing the training in {timeSpent} mins." 
                print(msg)
                # api call to /v1/notify
                try: 
                    message_data = {'message': msg}
                    notify = requests.post(NOTIFY_MICROSERVICE_URL + '/v1/notify' , json=message_data)
                except:
                    serviceUnavailable("notification")
                del cache[newEvent.userId]
        elif(newEvent.userId in cache.keys() and cache[newEvent.userId].getType() == APP_LAUNCH and newEvent.type == TRAINING_FINISH): 
            print("Exception - Invalid series of events.")   
        else:
            cache[newEvent.userId] = newEvent
    return '', 204

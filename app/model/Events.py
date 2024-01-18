from ..constants import DATE_FORMAT
from datetime import datetime

class Event:
    def __init__(self, userId, type,timestamp, trainingId = 0) -> None:
        self.userId = userId
        self.type = type
        self.trainingId = trainingId
        self.timestamp = datetime.strptime(timestamp, DATE_FORMAT)

    def getUserId(self):
        return self.userId
        
    def getType(self):
        return self.type
        
    def getTrainingId(self):
        return self.trainingId
        
    def getTimestamp(self):
        return self.timestamp
        
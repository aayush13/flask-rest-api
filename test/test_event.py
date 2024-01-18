import unittest
import requests

class EventApiTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    

    def testcase1(self):
        testEvent = {
            "user_id": "foo2",
            "device_id": "bar2",
            "type": "app_launch",
            "time_stamp": "2021-02-28 16:22:52"   
        }
        response = requests.post(url = "http://127.0.0.1:5000/v1/event/", json=testEvent)
        self.assertEqual(response.status_code, 204)
        print("Testcase 1 - API responds back successfully with code 204")
    
    def testcase2(self):
        testEvent = {
            "user_id": "foo2",
            "device_id": "bar2",
            "type": "app",
            "time_stamp": "2021-02-28 16:22:52"   
        }
        response = requests.post(url = "http://127.0.0.1:5000/v1/event/", json=testEvent)
        self.assertEqual(response.text, '')
        print("Testcase 2 - API responds back successfully with empty body")
        


if __name__ == '__main__':
    testEventApi = EventApiTest()
    testEventApi.testcase1()
    testEventApi.testcase2()
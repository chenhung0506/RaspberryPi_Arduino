import requests
import json

def change_face_id(msg):
<<<<<<< Updated upstream
    firebase_url = 'https://你的.firebaseio.com/'
=======
    firebase_url = 'https://arduino-d6136-default-rtdb.firebaseio.com/'
>>>>>>> Stashed changes
    data = {'faceid':msg}
    result = requests.put(firebase_url + '/opencv.json', verify=True, data=json.dumps(data))
    print(result)


if __name__ == '__main__':
    change_face_id('ok')

# pip install firebase-admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://.firebaseio.com/'
})

# 要監聽的路徑
ref = db.reference('opencv/faceid')

def listener(event):
    #print(event.event_type)  # can be 'put' or 'patch'
    #print(event.path)  # relative to the reference, it is empty in this case
    print(event.data)  # new data at /reference/event.path. None if deleted

if __name__ == '__main__':
    # Attach the callback function to the reference
    ref.listen(listener)

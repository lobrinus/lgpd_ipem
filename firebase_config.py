import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyB5chTFihZM_v-5bkVecmDDUvkOKG7C22Q",
    "authDomain": "lgpd-ipem-mg-9f1a5.firebaseapp.com",
    "projectId": "lgpd-ipem-mg-9f1a5",
    "storageBucket": "lgpd-ipem-mg-9f1a5.appspot.com",
    "messagingSenderId": "XXXXXXXXXXXX",
    "appId": "1:XXXXXXXXXXXX:web:XXXXXXXXXXXX",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

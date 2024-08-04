import pyrebase

config = {
    "apiKey": "AIzaSyBhnV-C-cDQKdaD9lyhBDlvYG3logY3xoY",
    "authDomain": "fir-dbtest-4fdf7.firebaseapp.com",
    "projectId": "fir-dbtest-4fdf7",
    "databaseURL": "https://fir-dbtest-4fdf7-default-rtdb.firebaseio.com",
    "storageBucket": "fir-dbtest-4fdf7.appspot.com",
    "messagingSenderId": "822623979316",
    "appId": "1:822623979316:web:94789dcff9b1d46ff24761",
    "measurementId": "G-Q2RFRWPJ77"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# data = {"username": "admin",
#         "admin_status" : True
#         }

data = {"id": 1,
        "name": 'John',
        "age": 25,
        "job_status": False
    }

# ---------------------------------------------------------------
# create Data or add a data node (record)

# it gerneate a random node and save record init

# database.push(data)

# specify the child node name and set data
# database.child("users").set(data)

# ---------------------------------------------------------------
# get Data

# users = database.child("users").get()
# print(users.val())

# ---------------------------------------------------------------
# Update Data

# database.child("users").update({"age": 50})

# ---------------------------------------------------------------
# remove data

# delete single data (age data)
# database.child("users").child("age").remove()

# delete main node users
# database.child("users").remove()
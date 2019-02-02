# Home Cloud written in Python3
## Installation
#### 1.
```sh
$ pip install -r requirements.txt
```
#### 2.
You have to change the "host" variable to your locale ipadress at the end of the file.
>     app.run(
>        debug=False,
>        host= '192.168.180.40',# set your ip here
>        threaded=True,
>        port = 80
>        )
#### 3.
You should change the "mypassword" variable to a secret password.
    
>       app = Flask(__name__)
>       mypassword = 'password'#set your password here
>       app.config['UPLOAD_FOLDER'] = 'uploads'
## Run your server
```sh
$ python server.py
```
Then open your browser and use your IP as URL.
### Features
- File Upload
- Delete files
- Login
- List files

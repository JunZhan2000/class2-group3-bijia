from flask import Flask


app = Flask('bijia')
app.config.from_pyfile('settings.py')
app.secret_key='secret key'



from bijia import views, errors
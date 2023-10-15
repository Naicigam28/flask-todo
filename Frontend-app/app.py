import requests
from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def index():
    r = requests.get('http://backend:5000/todos')
    res=r.json()
    print(res)
    return render_template('index.html', todos=res)

if __name__=="__main__":
    app.run(debug=True)

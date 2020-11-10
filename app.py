from flask import Flask, render_template
import requests

app = Flask(__name__)

def safe_string(string):
    return ''.join([c for c in string if c.isalnum() or c in ['.','-','_']])

@app.route('/api/followers/<username>')
def followers(username):
    username = safe_string(username)
    r = requests.get('https://instagram.com/'+username)
    token = '"edge_followed_by":{"count":'
    start = r.text.find(token) 
    start += len(token)
    end = r.text.find('}',start)
    followers = r.text[start:end]
    return followers

@app.route('/api/picture/<username>')
def picture(username):
    username = safe_string(username)
    r = requests.get('https://instagram.com/'+username)
    token = 'profile_pic_url":"'
    start = r.text.find(token) 
    start += len(token)
    end = r.text.find('",', start)
    profile_url = r.text[start:end].replace("\\u0026", "&")
    return profile_url

@app.route('/<username>')
def index(username):
    username = safe_string(username)
    return render_template('index.html', username=username, followers=followers(username), picture=picture(username))

@app.route('/')
def default_index():
    return index("j.olavarria.m")

if __name__ == '__main__':
    app.run(debug = True)
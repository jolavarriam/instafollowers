from flask import Flask, render_template, send_file
import requests

app = Flask(__name__)

def safe_string(string):
    return ''.join([c for c in string if c.isalnum() or c in ['.','-','_']])

@app.route('/api/followers/<username>')
def followers(username):
    username = safe_string(username)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get('https://instagram.com/'+username, headers=headers)
    text_file = open("requests.txt", "wb")
    text_file.write(r.content)
    text_file.close()
    print(r)
    token = '"userInteractionCount":"'
    start = r.text.find(token) 
    start += len(token)
    end = r.text.find('"}',start)
    followers = r.text[start:end]
    path = "requests.txt"
    return send_file(path, as_attachment=True)
    #return followers

@app.route('/api/picture/<username>')
def picture(username):
    username = safe_string(username)
    r = requests.get('https://instagram.com/'+username)
    token = 'profile_pic_url":"'
    start = r.text.find(token) 
    start += len(token)
    end = r.text.find('",', start)
    profile_url = r.text[start:end].replace("\\u0026", "&")
    #print(profile_url)
    return profile_url

@app.route('/<username>')
def index(username):
    username = safe_string(username)
    return followers(username) 
    #return render_template('index.html', username=username, followers=followers(username), picture=picture(username))

@app.route('/')
def default_index():
    return index("j.olavarria.m")

if __name__ == '__main__':
    app.run(debug = True)
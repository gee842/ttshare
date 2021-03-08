from flask import Flask
import flask
from flask import request
import base64
import pickle
import random
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

from app.tts import comment_to_mp3


@app.route('/save', methods=['GET'])
def save_mp3():
    try:
        
        text = request.args.get('text', default=1, type=str)
        if len(text>1000):
            return 'Keep it under 1000 chars pls (free tier google cloud)'
        saved_id = ''.join(random.choice('0123456789abcdef') for n in range(30))
        comment_to_mp3(text,"./quota.txt",saved_id,randomize=True)
        return saved_id
    except Exception as e:
        return e.message()
    
@app.route('/mp3s', methods=['GET'])      
def get_mp3():
    #test if exists then throw error accordingly
    tts_id = request.args.get('tts_id', default=1, type=str)
    return flask.send_file('/saved/{tts_id}.mp3',as_attachment=True)

    
    


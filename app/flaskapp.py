from flask import Flask
import flask
from flask_cors import CORS, cross_origin
from flask import request
import base64
import pickle
import random
app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
names_list = ["en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D", "en-GB-Wavenet-F", "en-AU-Wavenet-A", "en-AU-Wavenet-B", "en-AU-Wavenet-C", "en-AU-Wavenet-D","en-US-Wavenet-G","en-US-Wavenet-H","en-US-Wavenet-I","en-US-Wavenet-J","en-US-Wavenet-A","en-US-Wavenet-B","en-US-Wavenet-C","en-US-Wavenet-D","en-US-Wavenet-E","en-US-Wavenet-F","en-US-Standard-B","en-US-Standard-C","en-US-Standard-D","en-US-Standard-E","en-US-Standard-G","en-US-Standard-H","en-US-Standard-I","en-US-Standard-J", "en-AU-Standard-A", "en-AU-Standard-B", "en-AU-Standard-C", "en-AU-Standard-D", "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Standard-F"]
from app.tts import comment_to_mp3


@app.route('/save', methods=['GET'])
@cross_origin()
def save_mp3():
    try:
        selected_voice = request.args.get('voice', default='Random', type=str)
        text = request.args.get('text', default='please provide text', type=str)
        if len(text)>1000:
            return 'Keep it under 1000 chars pls (free tier google cloud)'
        saved_id = ''.join(random.choice('0123456789abcdef') for n in range(30))
        if selected_voice == 'Random':
            comment_to_mp3(text,"./quota.txt",saved_id,randomize=True)
            return saved_id
        elif selected_voice not in names_list:
            return 'Error, voice not found'
        else:
            comment_to_mp3(text,"./quota.txt",saved_id,randomize=False,voice=selected_voice)
            return saved_id
            
    except Exception as e:
        return e.message()
    
@app.route('/mp3s', methods=['GET'])      
@cross_origin()
def get_mp3():
    #test if exists then throw error accordingly
    tts_id = request.args.get('tts_id', default=1, type=str)
    return flask.send_file(f'../saved/{tts_id}.mp3',as_attachment=True)

    
    


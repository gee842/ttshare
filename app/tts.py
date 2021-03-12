# $env:GOOGLE_APPLICATION_CREDENTIALS="D:\Downloads\redditvidtts-2242083b8e66.json"
#todo: user voice selection, playable embed
from google.cloud import texttospeech
import json
import random
import os
import re

names_list = ["en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D", "en-GB-Wavenet-F", "en-AU-Wavenet-A", "en-AU-Wavenet-B", "en-AU-Wavenet-C", "en-AU-Wavenet-D","en-US-Wavenet-G","en-US-Wavenet-H","en-US-Wavenet-I","en-US-Wavenet-J","en-US-Wavenet-A","en-US-Wavenet-B","en-US-Wavenet-C","en-US-Wavenet-D","en-US-Wavenet-E","en-US-Wavenet-F","en-US-Standard-B","en-US-Standard-C","en-US-Standard-D","en-US-Standard-E","en-US-Standard-G","en-US-Standard-H","en-US-Standard-I","en-US-Standard-J", "en-AU-Standard-A", "en-AU-Standard-B", "en-AU-Standard-C", "en-AU-Standard-D", "en-GB-Standard-A", "en-GB-Standard-B", "en-GB-Standard-C", "en-GB-Standard-D", "en-GB-Standard-F"]

def comment_to_mp3(input_text, FILEPATH_QUOTA,POST_ID,randomize=False,voice='en-US-Wavenet-H'):
    num_of_chars = len(input_text)

    with open(FILEPATH_QUOTA, 'r') as f:
        line = f.readline()
        quota_remaining = int(line)
        if quota_remaining < num_of_chars+100:
            raise Exception("Quota depleted :(")
    
    if randomize:
        selected_voice = random.choice(names_list)
        print(f"RANDOM VOICE = {selected_voice}")

    else:
        selected_voice = voice

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=input_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name=selected_voice
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(FILEPATH_QUOTA, 'w') as f:
        quota_remaining -= num_of_chars
        print(f"-----QUOTA REMAINING: {quota_remaining}-----")
        f.write(str(quota_remaining))

    filename = input_text[0:8].replace(".","").replace("*","")
    filename = re.sub('[\W_]+', '', filename) 



    with open(f"./saved/{POST_ID}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "{POST_ID}.mp3"')


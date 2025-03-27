from flask import Flask, jsonify, request
import speech_recognition as sr
import subprocess
import time
import threading
import pyttsx3
import os

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to unlock the screen
def unlock_screen():
    print("Wake word detected! Waking up device...")
    
    # Wake the device using ADB (replace with Appium commands if needed)
    subprocess.run(["adb", "shell", "input keyevent POWER"])
    time.sleep(1)
    subprocess.run(["adb", "shell", "input swipe 500 1500 500 500"])  # Swipe to unlockx

    print(""
    "unlocked!")
    
    # Speak the message
    speak("Please unlock your mobile phone")
    
    return "Please unlock your mobile phone"

# Function to listen for the wake word
def listen_for_wake_word(command):
    print(f"Received: {command}")

    if "hey jolly" in command.lower():
        message = unlock_screen()
        return message
    
    return "Wake word not detected"


@app.route('/start-listening', methods=['POST'])
def start_listening():
    data = request.get_json()
    command = data.get("command", "")

    response = listen_for_wake_word(command)
    return jsonify({"message": response})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Vercel's port
    app.run(host='0.0.0.0', port=port)

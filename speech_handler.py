import speech_recognition as sr
import pyttsx3
#import pygame
import simpleaudio  as sa
import sounddevice as sd
import time, os, sys


class SpeechAssistant:

    def __init__(self, keyword = "alpha",listen_timeout = 30, speech_timeout = 30,speech_duration = 10):
        
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        #self.tts_engine.setProperty('voice', 'english')  # Or any other voice you prefer
        self.tts_engine.setProperty('rate', 170)  # Adjust the speech rate if needed

        # Set the output audio driver (use 'espeak' to avoid conflicts)
        self.tts_engine.setProperty('driverName', 'espeak')

        
        self.keyword = keyword
        self.listen_timeout = listen_timeout  # Timeout for keyword detection
        self.speech_timeout = speech_timeout  # Timeout for speech detection in seconds
        self.speech_duration = speech_duration  # Duration of each speech listening window in seconds
        #pygame.mixer.init()
        self.play_sound()
        
        time.sleep(2)
        
    
    def speak_text(self, text):
        """Convert text to speech."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()


    def play_sound(self):
        wave_obj = sa.WaveObject.from_wave_file("/home/robo/robodog/rpi/sound.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        #pygame.mixer.music.load("/home/robo/robodog/rpi/sound.wav")
        #pygame.mixer.music.play()


    def play_beep(self):
        """
        Plays a beep sound to indicate that the assistant is listening.
        """

        wave_obj = sa.WaveObject.from_wave_file("/home/robo/robodog/rpi/beep.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        #pygame.mixer.music.load("/home/robo/robodog/rpi/beep.wav")  # Load the beep sound (ensure the file exists)
        #pygame.mixer.music.play()


    # Function to handle keyword detection indefinitely
    def listen_for_keyword(self):
        """
        Listens indefinitely for a specific keyword. Resets after a 30-second timeout
        if no keyword is detected.
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Filter out background noise
            start_time = time.time()
            prompt_time = time.time()  # Track when the prompt was last spoken

            while True:
                # Check for timeout (30 seconds without detecting the keyword)
                if time.time() - start_time > self.listen_timeout:
                    print("Timeout! Restarting keyword detection...")
                    start_time = time.time()

                try:
                    # Only say the prompt every 10 seconds (or any interval you choose)
                    if time.time() - prompt_time > 10:  # Only repeat every 10 seconds
                        self.speak_text("Say Hi Alpha if you need my help.")
                        time.sleep(2)
                        self.play_beep()
                        prompt_time = time.time()  # Reset the prompt time after speaking

                    print(f"Listening for keyword...{self.keyword}")
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    recognized_text = self.recognizer.recognize_google(audio).lower()
                    print(f"Recognized: {recognized_text}")

                    if self.keyword in recognized_text:
                        print(f"Keyword '{self.keyword}' detected!")
                        return True  # Move to next phase
                    elif "sleep" in recognized_text:
                        sys.exit()

                except sr.UnknownValueError:
                    # If speech is unintelligible, ignore and continue
                    continue

                except sr.RequestError:
                    print("Error")
                    break

    # Function to listen for general speech every 7 seconds
    def listen_for_speech(self):
        """
        Listens for speech every 7 seconds. If no speech is detected for 30 seconds,
        returns to keyword listening phase.
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            last_detection_time = time.time()
            
            while True:
                if time.time() - last_detection_time > self.speech_timeout:
                    print("No speech detected for 30 seconds. Returning to keyword detection...")
                    return  # Return to keyword detection phase

                try:
                    
                    self.play_beep()
                    print("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout= self.speech_duration, phrase_time_limit = self.speech_duration)

                    try:
                        recognized_text = self.recognizer.recognize_google(audio).lower()
                        print(f"Recognized speech: {recognized_text}")
                        # Reset 30-second timer on speech detection
                        last_detection_time = time.time()
                        return recognized_text

                    except sr.UnknownValueError:
                        print("No intelligible speech detected. Listening again...")
                        continue

                except sr.WaitTimeoutError:
                    # If no speech within 7 seconds, continue looping
                    print("No speech detected")
                    continue


    def navigation(self):
        for i in range (20):
            print(f"nav_{i}") 
            time.sleep(2)
        return True
    
    
    def start_interaction(self):
        navigation = False
        while True:
            if self.listen_for_keyword():
                self.speak_text("How may I help you?")
                #self.play_beep()
                recognized_text = self.listen_for_speech()
                if recognized_text:
                    result= self.navigation()
                    if result == True:
                        self.speak_text("Navigation completed. Thank you for visiting")
                        time.sleep(3)
                        continue
                    
                

if __name__ == "__main__":
    
    speechassistant = SpeechAssistant(keyword= "alpha", listen_timeout=30, speech_timeout=30, speech_duration=10 )
    navigation = False
    while True:
        if speechassistant.listen_for_keyword():
            speechassistant.speak_text("How may I help you?")
            #self.play_beep()
            recognized_text = speechassistant.listen_for_speech()
            if recognized_text:
                result= speechassistant.navigation()
                if result == True:
                    speechassistant.speak_text("Navigation completed. Thank you for visiting")
                    time.sleep(3)
                    continue
    

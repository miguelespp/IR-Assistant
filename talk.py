import os
import time
from pygame import mixer
import fakeyou


class Talk:
    def __init__(self, username, password, model_name):
        self.username = username
        self.password = password
        self.model_name = model_name
        self.fake_you = fakeyou.FakeYou()
        self.__login_to_fakeyou()

    def __login_to_fakeyou(self):
        self.fake_you.login(self.username, self.password)

    def __generate_audio(self, text):
            tts_model_token = "weight_s0zjjkmht28dp4gm83e6xvjdk"
            locucion = self.fake_you.say(text=text, ttsModelToken=tts_model_token)
            locucion.save("temp.wav")
            filename = "temp.wav"
            return filename

    def talk(self, text):
        mixer.init()
        filename = self.__generate_audio(text)
        mixer.music.load(filename)
        audio_duration = mixer.Sound(filename).get_length()
        mixer.music.play()
        time.sleep(audio_duration)
        mixer.music.stop()
        mixer.quit()
        os.remove(filename)
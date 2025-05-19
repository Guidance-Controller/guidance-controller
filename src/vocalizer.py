import pyttsx3
import threading

class Vocalizer:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.lock = threading.Lock()
        self._utter_thread = None
        self._is_uttering = False

    def is_uttering(self) -> bool:
        with self.lock:
            return self._is_uttering

    def _speak(self, phrase: str):
        with self.lock:
            self._is_uttering = True
        self.engine.say(phrase)
        self.engine.runAndWait()
        with self.lock:
            self._is_uttering = False

    def utter(self, phrase: str, interupt: bool = False) -> bool:
        if self.is_uttering():
            if not interupt:
                return False
            else:
                self.engine.stop()
                if self._utter_thread and self._utter_thread.is_alive():
                    self._utter_thread.join()

        self._utter_thread = threading.Thread(target=self._speak, args=(phrase,))
        self._utter_thread.start()
        return True
import pyttsx3
import threading
import queue

class Vocalizer:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        self._is_uttering = False
        self._lock = threading.Lock()

        # Start the background thread
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            phrase = self.queue.get()
            if phrase is None:
                break  # Optional: stop signal
            with self._lock:
                self._is_uttering = True
            self.engine.say(phrase)
            self.engine.runAndWait()
            with self._lock:
                self._is_uttering = False

    def is_uttering(self) -> bool:
        with self._lock:
            return self._is_uttering

    def utter(self, phrase: str, interupt: bool = False) -> bool:
        if self.is_uttering():
            if not interupt:
                return False
            else:
                self.engine.stop()  # Force stop current speech
        self.queue.put(phrase)
        return True
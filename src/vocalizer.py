import os
import time
import subprocess


class Vocalizer:
    def __init__(self, buffer_period: float = 0.5) -> None:
        self.buffer_period = buffer_period
        self.last_utter_time = time.time() - buffer_period

    def is_uttering(self) -> bool:
        result = subprocess.run(
            ['pgrep', 'say'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0

    def utter(self, phrase: str, interupt: bool = False) -> bool:
        if phrase == "":
            return False

        if interupt:
            os.system(f'killall say; say "{phrase}" &')
            self.last_utter_time = time.time()
            return True

        elif time.time() - self.last_utter_time >= self.buffer_period:
            if self.is_uttering():
                return False

            subprocess.Popen(['say', f'"{phrase}"'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

            self.last_utter_time = time.time()
            return True

        else:
            return False
## app/adivinarnumero/adivinarnumero.py

import random, time
from globals.constants import NUM_ATTEMPTS, NUM_WIN, NUM_LOSS, TIME_BONUS

class AdivinarNumero:
    def __init__(self, session_data):
        self.target = session_data.get('target', random.randint(1, 100))
        self.attempts = session_data.get('attempts', 0)
        self.max_attempts = NUM_ATTEMPTS
        self.score = session_data.get('score', 0)
        self.start_time = session_data.get('start_time', time.time())

    def guess(self, number):
        self.attempts += 1
        result = None
        finished = False

        if number == self.target:
            elapsed = int(time.time() - self.start_time)
            bonus = max(TIME_BONUS - elapsed, 0)
            self.score += NUM_WIN + bonus
            result = 'correct'
            finished = True
        elif number < self.target:
            result = 'low'
        else:
            result = 'high'

        if self.attempts >= self.max_attempts and result != 'correct':
            self.score += NUM_LOSS
            result = 'fail'
            finished = True

        return {
            'status': 'success',
            'result': result,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'score': self.score,
            'finished': finished,
            'elapsed': int(time.time() - self.start_time),
        }

    def get_state(self):
        return {
            'target': self.target,
            'attempts': self.attempts,
            'score': self.score,
            'start_time': self.start_time,
        }

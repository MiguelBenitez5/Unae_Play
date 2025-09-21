# app/piedrapapeltijera/piedrapapeltijera.py

import random

class PiedraPapelTijera:
    def __init__(self, session_data):
        self.score = session_data.get('score', 0)
        self.player_wins = session_data.get('player_wins', 0)
        self.machine_wins = session_data.get('machine_wins', 0)
        self.draws = session_data.get('draws', 0)
        self.choices = ['piedra', 'papel', 'tijera']
        
    def play_round(self, player_choice):
        machine_choice = random.choice(self.choices)
        result = self.__determine_winner(player_choice, machine_choice)
        
        if result == 'win':
            self.player_wins += 1
            self.score += 10
        elif result == 'defeat':
            self.machine_wins += 1
            self.score -= 5
        else:
            self.draws += 1
            self.score += 2

        return {
            'status': 'success',
            'player_choice': player_choice,
            'machine_choice': machine_choice,
            'result': result,
            'score': self.score,
            'player_wins': self.player_wins,
            'machine_wins': self.machine_wins,
            'draws': self.draws,
        }

    def __determine_winner(self, player, machine):
        if player == machine:
            return 'draw'
        
        if (player == 'piedra' and machine == 'tijera') or \
           (player == 'papel' and machine == 'piedra') or \
           (player == 'tijera' and machine == 'papel'):
            return 'win'
        
        return 'defeat'

# app/piedrapapeltijera/piedrapapeltijera.py

import random
from globals.constants import RPS_ROUNDS, RPS_WIN, RPS_DRAW, RPS_LOSS

class PiedraPapelTijera:
    def __init__(self, session_data):
        self.player_score = session_data.get('player_score', 0)
        self.player_wins = session_data.get('player_wins', 0)
        self.machine_wins = session_data.get('machine_wins', 0)
        self.draws = session_data.get('draws', 0)
        self.rounds_played = session_data.get('rounds_played', 0)
        self.choices = ['piedra', 'papel', 'tijera']

    def play_round(self, player_choice):
        # Validar elección
        if player_choice not in self.choices:
            return {
                'status': 'error',
                'message': f'Elección inválida: {player_choice}. Debe ser piedra, papel o tijera.'
            }

        # Verificar si ya se alcanzó el límite de rondas
        if self.rounds_played >= RPS_ROUNDS:
            return {
                'status': 'finished',
                'message': 'El juego ha terminado. Reinicia para jugar de nuevo.',
                'player_score': self.player_score,
                'player_wins': self.player_wins,
                'machine_wins': self.machine_wins,
                'draws': self.draws,
                'rounds_played': self.rounds_played,
            }

        machine_choice = random.choice(self.choices)
        result = self.__determine_winner(player_choice, machine_choice)

        # Actualizar estado del juego
        self.rounds_played += 1
        if result == 'win':
            self.player_wins += 1
            self.player_score += RPS_WIN
        elif result == 'defeat':
            self.machine_wins += 1
            self.player_score += RPS_LOSS
        else:
            self.draws += 1
            self.player_score += RPS_DRAW

        return {
            'status': 'success',
            'player_choice': player_choice,
            'machine_choice': machine_choice,
            'result': result,
            'player_score': self.player_score,
            'player_wins': self.player_wins,
            'machine_wins': self.machine_wins,
            'draws': self.draws,
            'rounds_played': self.rounds_played,
            'rounds_limit': RPS_ROUNDS,
        }

    def get_state(self):
        """Devuelve solo el estado relevante para guardar en sesión."""
        return {
            'player_score': self.player_score,
            'player_wins': self.player_wins,
            'machine_wins': self.machine_wins,
            'draws': self.draws,
            'rounds_played': self.rounds_played,
        }

    def __determine_winner(self, player, machine):
        if player == machine:
            return 'draw'

        if (player == 'piedra' and machine == 'tijera') or \
           (player == 'papel' and machine == 'piedra') or \
           (player == 'tijera' and machine == 'papel'):
            return 'win'

        return 'defeat'
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from tateti import Tateti
import time, secrets

# Create your views here.

def renderPage(request):
    #comprobar que el usuario esta loguedado para acceder al juego
    access = request.session.get('access')
    if not access:
        return HttpResponseRedirect('url_de_login')
    #aqui se pasa la logica que se quiera renderizar en la pagina 
    return render(request, 'tateti.html')

"""
Realiza la jugada, recibiendo la peticion del cliente y envia los resultados a traves de on JSON\n
Estados retornados:
    -status : error (cuando la jugada es incorrecta)
    -status : success (cuando la jugada se realizo correctamente)
Estado de la partida retornados:
    -game_status : 0 (la partida continua, aun no esta definodo el ganador o empate)
    -game_status : win (el jugador gana la partida, es decir logra vencer a la maquina en todas sus dificultades)
"""
def playTateti(request,position):
    row = int(position[0])
    column = int(position[2])

    #guardar los datos en la sesion
    def saveSession(board, playerMoves, machineMoves, level):
        request.session['tateti']['board'] = board
        request.session['tateti']['player_moves'] = playerMoves
        request.session['tateti']['macine_moves'] = machineMoves
        request.session['tateti']['level'] = level

    #crear una sesion si aun no existe una
    if 'tateti' not in request.session:
        board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        request.session['tateti'] = {
            'token': secrets.token_hex(16),
            'start_time' : time.time(),
            'board': board,
            'player_moves': 0,
            'machine_moves': 0,
            'level':'easy'
        }  
    #cargar los datos de la sesion en una variable
    data = request.session.get('tateti')
    
    #se crea el objeto tateti con los datos de la sesion    
    tateti = Tateti(data['board'],data['player_moves'],data['machine_moves'],data['level'])

    #lugar para dialogos si ocurre en el futuro

    #se guarda la jugada del jugador en una variable
    playerPlay = tateti.playPlayer(row, column)
    #se verifica si la jugada del jugador es valida y se retorna error en caso de no ser una jugada valida
    if not playerPlay:
        response = {
            'status': 'error'
        }
        return JsonResponse(response)
    
    #sumar una jugada al jugador
    data['player_moves'] += 1

    #comprobar tablero luego de la jugada del jugador
    check = tateti.checkBoard()

    if check is 1:
        response = {
            'status' : 'success',
            'game_status' : 'win'
        }
        
        #aqui deberia calcularse el puntaje del jugador y tal vez guardarlo en la sesion
        
        if data['level'] == 'easy':
            data['level'] = 'medium'
        elif data['level'] == 'medium':
            data['level'] = 'hard'
        else:
            response['game_status'] = 'win_game'
            #si el jugador gana deberia colocar su puntaje en la base de datos
            try:
                del request.session['tateti']
            except:
                pass
        saveSession(tateti.restartBoard(),data['player_moves'],data['machine_moves'],data['level'])
        response['level'] = data['level']
        return JsonResponse(response)
    
    if check is 0 and data['player_moves'] >= 5:
        response = {
            'status' : 'success',
            'game_status' : 'draw'
        }
        saveSession(tateti.restartBoard(), 0, 0, data['level'])
        return JsonResponse(response)
    
    #juega la maquina
    machinePlay = tateti.playMachine()
    data['machine_moves'] += 1

    check = tateti.checkBoard()

    if check is -1:
        response = {
            'status' : 'success',
            'game_status' : 'defeat'
        }
        try:
            del request.session['tateti']
        except:
            pass

        return JsonResponse(response)
    
    if check is 0 and data['machine_moves'] >= 5:
        response = {
            'status' : 'success',
            'game_status' : 'draw'
        }
        saveSession(tateti.restartBoard(),0,0,data['level'])
        return JsonResponse(response)
    
    #si no gana ninguno se retorna un JSON con los datos de la partida y se guardan en sesion
    response = {
        'status' : 'success',
        'game_status' : 0,
        'machine_play' : machinePlay,
    }

    saveSession(tateti.getBoard(), data['player_moves'],data['machine_moves'], data['level'])

    return JsonResponse(response)

def restartGame(request):
    try:
        del request.session['tateti']
        return JsonResponse({'status': 'success', 'message': 'La sesion fue eliminada correctamente'})
    except:
        return JsonResponse({'status': 'error', 'message': 'No se pudo eliminar la sesion'})


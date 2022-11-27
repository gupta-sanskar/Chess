from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from game.models import GameMoves
import urllib.request
import chess
import chess.svg
import chess.pgn

# Create your views here.
board = chess.Board()
game = chess.pgn.Game()
allmoves = GameMoves()

# Home Page
def home(request):
    return render(request, 'home.html')

# Handles User Registration
def handleRegister(request):
    if request.method == "POST":
        # Getting parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Error Check
        if len(username)>30:
            messages.error(request, "Username must be under 30 characters")
            return render(request, 'home.html')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return render(request, 'home.html')
        if not username.isalnum():
            messages.error(request, "Username should not contain special characters")
            return render(request, 'home.html')

        # Creating User
        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request, "Your account has been created successfully")
        messages.success(request, "You may now login")
        return render(request, 'home.html')
    else:
        messages.error(request, "Invalid response")
        return render(request, 'home.html')

# Handles User Login
def handleLogin(request):
    if request.method == "POST":
        # Getting parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!!")
        else:
            messages.error(request, "Invalid Credentials, Please try again!")
        return render(request, 'login.html')

# Handles User Logout
def handleLogout(request):
    logout(request)
    messages.success(request, "Logged out Successfully!!")
    return render(request, 'home.html')

# Displays Board
def linker(request):
    if request.method == "POST":
        return render(request, 'game.html',{'board':board})

# Getting move from User
def getmove(request):
    if request.method == "POST":
        move = request.POST['move']
        makemove(move)
        return render(request, 'game.html')

# Makes move
def makemove(move):
    try:
        while not board.is_game_over():
            if board.turn == True:
                board.push_san(move)
                board.turn = False
                savegamestate(move)
                gamestatus()
            elif board.turn == False:
                board.push_san(move)
                savegamestate(move)
                gamestatus()
            else:
                print("wrong move")
                break
    except Exception as e:
        print(e)

    print(board)
    return redirect(linker)

# Decides which color
def who():
    if board.turn == chess.WHITE:
        return str("BLACK")
    else:
        return str("WHITE")

# Gives the status of game
def gamestatus():
    if board.is_checkmate():
        print("Checkmate " + who() + " wins!")
        moves_list = allmoves.get_list()
        for moves in moves_list:
           print(moves)
    elif board.is_stalemate():
        print("Game drawn : Stalemate")

# Saves game state to be used to show boardstate
def savegamestate(move):
    node = game.add_variation(move)
    allmoves.set_list(move)

# Board at specific move
def boardstate(request):
    if request.method == "POST":
        for number, move in enumerate(game.mainline_moves()):
            pass
    return HttpResponse(chess.svg.board(board=board, size=650), content_type='image/svg+xml')

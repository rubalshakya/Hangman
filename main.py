
from flask import Flask,request,render_template
from Hangman_game import Hangman,hangman_images
player = Hangman()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    

@app.route("/play",methods=["POST","GET"])
def play():
    if request.method == "POST":
        if request.form["want_to_play"]=="Yes":
            ask_inputs = player.play()
            return render_template("guess.html",result=ask_inputs)
        else:
            return render_template("not_play.html")


@app.route("/guess",methods=["POST","GET"])
def guess():
     if request.method == "POST":
         user_guess = request.form["Guessed_letter"]
         Result = player.guess_letter(user_guess)
         if Result["game_status"]=="on":
             return render_template("guess_1.html",result=Result)
         elif Result["game_status"]=="lose":
             return render_template("lose.html",result=Result)
         elif Result["game_status"]=="win":
             return render_template("win.html",result=Result)
             

@app.route("/guess_1",methods=["POST","GET"])
def guess_1():
     if request.method == "POST":
         user_guess = request.form["Guessed_letter"]
         Result = player.guess_letter(user_guess)
         if Result["game_status"]=="on":
             return render_template("guess_1.html",result=Result)
         elif Result["game_status"]=="lose":
             return render_template("lose.html",result=Result)
         elif Result["game_status"]=="win":
             return render_template("win.html",result=Result)

             
             
if __name__ == "__main__":
    app.run(debug=True,port=8080)

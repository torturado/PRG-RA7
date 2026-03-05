from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/') 
def home():
    return render_template("login.html") 

@app.route('/registre') 
def registre():
    return render_template("registre.html") 
if __name__ == '__main__':
    app.run(debug=True)

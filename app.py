from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_bcrypt import generate_password_hash,check_password_hash
from Databases import User

app = Flask(__name__)
app.secret_key = "bnvsdnvsfvdvkvnjvdvdkbvdsc"


@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/dashboad')
def dashboad():
    return render_template("dashboard.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password)
        User.create(name = name, email = email, password = password)
        flash("Account Created Successfully")
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User.get(User.email==email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Logged in Successfully")
                session['logged_in']=True
                session['name']=user.name
                session['id']=user.id
                return redirect(url_for('dashboad'))
        except User.DoesNotExist:
            flash("Wrong Username or Password")
    return render_template("login.html")



if __name__ == '__main__':
    app.run()

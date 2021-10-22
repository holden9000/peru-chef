from flask import render_template, redirect, session, request, flash
from peru_chef_app import app
from peru_chef_app.models.user import User
from peru_chef_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt =Bcrypt(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/contact')
def contact():
    return render_template("contact_us.html")


@app.route('/login')
def log_and_reg():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("log_and_reg.html")

@app.route('/grains')
def grains():
    return render_template("grains.html")
@app.route('/pastas')
def pasta():
    return render_template("pasta.html")
@app.route('/salsas')
def salsas():
    return render_template("salsa.html")
@app.route('/honeys-and-pastrys')
def honeys():
    return render_template("honeys.html")
@app.route('/natural-products')
def natural():
    return render_template("natural.html")
@app.route('/condoments')
def condoments():
    return render_template("condoments.html")
@app.route('/productos-institucionales')
def productos_institucionales():
    return render_template("Productos_Institucionales.html")
@app.route('/envasados')
def envasados():
    return render_template("ENVASADOS.html")



@app.route("/users/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        # we redirect to the template with the form.
        return redirect('/login')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.register_user(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route("/users/login", methods=["POST"])
def login():
    print("Start of login function")
    if User.validate_login(request.form):
        data = { "email" : request.form["email"] }
        user_in_db = User.get_user_by_email(data)
        print(user_in_db)
        if not user_in_db:
            print("Did not find the email")
            flash("Email not found", "error")
        else:
            print("We found the email")
            if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
                flash("Invalid Email/Password" , "error")
            else:
                session['user_id'] = user_in_db.id
                return redirect("/dashboard")

    return redirect('/login')
    # if not User.validate_login(request.form):
    #     # we redirect to the template with the form.
    #     return redirect('/')

    # # see if the username provided exists in the database
    # data = { "email" : request.form["email"] }
    # user_in_db = User.get_user_by_email(data)
    # if user_in_db is None:
    #     flash("Email not found", "error")
    #     return redirect('/')

    # # user is not registered in the db
    # if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
    #     # if we get False after checking the password
    #     flash("Invalid Email/Password" , "error")
    #     return redirect('/')

    # # if the passwords matched, we set the user_id into session
    # session['user_id'] = user_in_db.id
    # return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_user(data)
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/users/<int:user_id>")
def user(user_id):
    if "user_id" not in session:
        return redirect("/")
    user_data = {
        "id": user_id
    }
    user = User.get_user(user_data)
    data = {
        "user_id": user_id
    }
    user_posts = Post.get_user_posts(data)
    return render_template("user.html", user=user, user_posts=user_posts)

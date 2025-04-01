from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from utils.db import db
from models.olympics import *
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"


# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    medals = Medals.query.all()
    serialized_medals = [medal.to_dict() for medal in medals]  # Convert to dictionaries
    return render_template("index.html", medals=serialized_medals)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        flash("Invalid credentials, please try again.", "danger")
    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
        else:
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! Please sign in.", "success")
            return redirect(url_for("signin"))
    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("signin"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        return redirect(url_for("home"))

    return render_template("contactus.html")


@app.route("/events")
@login_required
def events():
    events = Events.query.all()
    return render_template("events.html",events=events)


@app.route("/add-country", methods=["GET", "POST"])
@login_required
def add_country():
    if request.method == "POST":
        # Fetch form data
        countrycode = request.form.get("countrycode")
        country = request.form.get("country")
        countrylong = request.form.get("countrylong")
        gold = int(request.form.get("gold", 0))
        silver = int(request.form.get("silver", 0))
        bronze = int(request.form.get("bronze", 0))
        total = gold + silver + bronze

        # Check if country already exists
        existing_country = Medals.query.filter_by(contrycode=countrycode).first()
        if existing_country:
            return "Country already exists!", 400

        # Add new country
        new_country = Medals(
            contrycode=countrycode,
            contry=country,
            contrylong=countrylong,
            gold=gold,
            silver=silver,
            bronze=bronze,
            total=total
        )
        db.session.add(new_country)
        db.session.commit()
        return redirect(url_for("home"))  # Redirect to the homepage

    return render_template("add_country.html")


@app.route("/update-medal/<countrycode>", methods=["GET", "POST"])
@login_required
def update_medal(countrycode):
    medal = Medals.query.filter_by(countrycode=countrycode).first_or_404()

    if request.method == "POST":
        try:
            medal.gold = int(request.form.get("gold"))
            medal.silver = int(request.form.get("silver"))
            medal.bronze = int(request.form.get("bronze"))
            medal.total = medal.gold + medal.silver + medal.bronze

            db.session.commit()
            flash("Medal counts updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for("home"))

    return render_template("update_medal.html", medal=medal)


@app.route("/delete-country/<countrycode>", methods=["POST"])
@login_required
def delete_country(countrycode):
    # Find the country by its countrycode
    country = Medals.query.filter_by(contrycode=countrycode).first()
    if country:
        db.session.delete(country)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return "Country not found!", 404


@app.route("/view-country/<countrycode>")
def view_country(countrycode):
    # Fetch country details
    country = Medals.query.filter_by(countrycode=countrycode).first()
    if not country:
        return "Country not found!", 404

    # Fetch players from the Players table
    players = Players.query.filter_by(countrycode=countrycode).all()
    medalists = Medalists.query.filter_by(countrycode=countrycode).all()

    return render_template("view_country.html", country=country, players=players, medalists=medalists)


@app.route("/add-player/<countrycode>", methods=["GET", "POST"])
@login_required
def add_player(countrycode):
    # Fetch country details for context
    country = Medals.query.filter_by(countrycode=countrycode).first()
    if not country:
        flash("Country not found!", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        gender = request.form.get("gender")
        events = request.form.get("events")

        # Validate inputs
        if not name or not gender or not events:
            flash("All fields are required!", "error")
            return render_template("add_player.html", country=country)

        # Add the player to the database
        new_player = Players(name=name, gender=gender, events=events, countrycode=countrycode, country=country.country)
        db.session.add(new_player)
        db.session.commit()

        flash(f"Player '{name}' added successfully!", "success")
        return redirect(url_for("view_country", countrycode=countrycode))

    return render_template("add_player.html", country=country)


@app.route("/update-player/<int:player_id>", methods=["GET", "POST"])
@login_required
def update_player(player_id):
    player = Players.query.get_or_404(player_id)

    if request.method == "POST":
        player.name = request.form.get("name")
        player.gender = request.form.get("gender")
        player.events = request.form.get("events")

        # Validate inputs
        if not player.name or not player.gender or not player.events:
            flash("All fields are required!", "error")
            return redirect(url_for("update_player", player_id=player.id))

        # Save updates to database
        db.session.commit()
        flash("Player updated successfully!", "success")
        return redirect(url_for("view_country", countrycode=player.countrycode))

    return render_template("update_player.html", player=player)


@app.route("/delete-player/<int:player_id>", methods=["POST"])
@login_required
def delete_player(player_id):
    player = Players.query.get_or_404(player_id)
    countrycode = player.countrycode

    try:
        db.session.delete(player)
        db.session.commit()
        flash("Player deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the player.", "error")

    return redirect(url_for("view_country", countrycode=countrycode))


@app.route("/add-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        event = request.form.get("event")
        tag = request.form.get("tag")
        sport = request.form.get("sport")
        sport_code = request.form.get("sport_code")
        sport_url = request.form.get("sport_url")

        if not event or not tag or not sport:
            flash("All fields are required!", "error")
            return redirect(url_for("add_event"))

        new_event = Events(event=event, tag=tag, sport=sport, sport_code=sport_code, sport_url=sport_url)
        db.session.add(new_event)
        db.session.commit()

        flash("Event added successfully!", "success")
        return redirect(url_for("events"))

    return render_template("add_event.html")


@app.route("/edit-event/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = Events.query.get_or_404(event_id)

    if request.method == "POST":
        try:
            event.event = request.form.get("event")
            event.tag = request.form.get("tag")
            event.sport = request.form.get("sport")
            event.sport_code = request.form.get("sport_code")
            event.sport_url = request.form.get("sport_url")

            db.session.commit()
            flash("Event updated successfully!", "success")
            return redirect(url_for("events"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "error")

    return render_template("edit_event.html", event=event)

@app.route("/delete-event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Events.query.get_or_404(event_id)
    try:
        db.session.delete(event)
        db.session.commit()
        flash(f"Events '{event.events}' deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")
    return redirect(url_for("events"))


@app.route("/add-medalist/<countrycode>", methods=["GET", "POST"])
@login_required
def add_medalist(countrycode):
    # Fetch country details to display in the form
    country = Medals.query.filter_by(countrycode=countrycode).first()
    if not country:
        flash("Country not found!", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        gender = request.form.get("gender")
        medal_type = request.form.get("medal_type")
        event = request.form.get("event")
        event_url = request.form.get("event_url")

        # Validate inputs
        if not name or not gender or not medal_type or not event or not event_url:
            flash("All fields are required!", "error")
            return render_template("add_medalist.html", country=country)

        # Create new medalist object and add to the database
        new_medalist = Medalists(
            name=name,
            gender=gender,
            medal_type=medal_type,
            countrycode=countrycode,
            country=country.country,
            event=event,
            event_url=event_url
        )
        db.session.add(new_medalist)
        db.session.commit()

        flash(f"Medalist '{name}' added successfully!", "success")
        return redirect(url_for("view_country", countrycode=countrycode))

    return render_template("add_medalist.html", country=country)


@app.route("/edit-medalist/<int:medalist_id>", methods=["GET", "POST"])
@login_required
def edit_medalist(medalist_id):
    medalist = Medalists.query.get_or_404(medalist_id)

    if request.method == "POST":
        medalist.name = request.form.get("name")
        medalist.gender = request.form.get("gender")
        medalist.medal_type = request.form.get("medal_type")
        medalist.event = request.form.get("event")
        medalist.event_url = request.form.get("event_url")

        db.session.commit()
        flash(f"Medalist '{medalist.name}' updated successfully!", "success")
        return redirect(url_for("view_country", countrycode=medalist.countrycode))

    return render_template("edit_medalist.html", medalist=medalist)


@app.route("/delete-medalist/<int:medalist_id>", methods=["POST"])
@login_required
def delete_medalist(medalist_id):
    medalist = Medalists.query.get_or_404(medalist_id)
    db.session.delete(medalist)
    db.session.commit()
    flash(f"Medalist '{medalist.name}' deleted successfully!", "success")
    return redirect(url_for("view_country", countrycode=medalist.countrycode))



with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(host='127.0.0.1',
            port=5000,
            debug=True
    )

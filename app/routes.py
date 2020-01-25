from flask import render_template
from app import app
from app.forms import CommentForm
import datetime

import sys
import os
db_path = os.path.join(sys.path[0], "app", "db")
c_path = os.path.join(sys.path[0], "app")
if db_path not in sys.path:
    sys.path.append(db_path)
if c_path not in sys.path:
    sys.path.append(c_path)
try:
    import dbconnect
except:
    from db import dbconnect

from carpenter import Carpenter

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = CommentForm()
    if form.validate_on_submit():

        c = Carpenter()

        name = form.name.data
        email = form.email.data
        comment = form.comment.data
        firstname = c.get_first_name(name)

        thank_you = "Thanks for visiting, {:}. We've sent your comment on to headquarters.".format(firstname)
        c.log_comment(name, email, comment)

        return render_template("contact_confirmation.html", title="Thanks!", thank_you=thank_you)

    return render_template('contact_form.html', title='Get in Touch', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/chooseTable")
def chooseTable():
    c = Carpenter()
    seasons = c.make_soccer_table("season", "Premier League")

    return render_template("chooseTable.html", title="Seasons", seasons=seasons)

@app.route("/chooseGraph")
def chooseGraph():
    c = Carpenter()
    seasons = c.make_soccer_table("season", "Premier League")

    return render_template("chooseGraph.html", title="Seasons", seasons=seasons)


@app.route("/chooseTeam")
def chooseTeam():
    c = Carpenter()
    teams = c.make_soccer_table("team", "Premier League")

    return render_template("chooseTeam.html", title="teams", teams=teams)


@app.route("/rain")
def rain():

    return render_template("rain.html", title="Rainfall")


@app.route("/<string:season>_graph")
def seasonGraph(season):
    c = Carpenter()
    c.tidy_data_folder()
    now = datetime.datetime.now()
    now = now.strftime("%f")
    filename_js = "{:}.csv".format(now)
    filename_py = "./app/static/js/{:}.csv".format(now)
    teams = c.get_season(season, "Premier League")
    title = season + " Premier League Season"
    c.create_csv(teams, filename_py)

    return render_template("pointsVgoals.html", filename=filename_js, title=title)

@app.route("/<string:season>_table")
def seasonTable(season):
    c = Carpenter()
    teams=c.get_season(season, "Premier League")
    title = season + " Premier League Season"

    return render_template("serveTable.html", teams=teams, title=title)


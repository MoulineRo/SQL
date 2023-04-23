import sqlite3

import flask
from faker import Faker

app = flask.Flask(__name__)


def fakename():
    fake = Faker()
    users = [fake.name() for i in range(10)]
    print(users)
    firstname = []
    for res2 in users:
        res3 = str(res2).replace('(', '').replace("'", '').split(' ')
        res4 = res3[0]
        firstname.append(res4)

    con = sqlite3.connect("cust.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS customers(name)")
    cur.executemany("""
        INSERT INTO customers VALUES(:name)
        """, zip(firstname))
    con.commit()


def faketrack():
    Faker.seed(0)
    fake = Faker()
    track = [fake.file_name(category='audio', extension='mp3') for x in range(10)]

    sec = [fake.random_int(min=150, max=220, step=1) for y in range(10)]

    con = sqlite3.connect("track.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS track(song,sec)")
    cur.executemany("""
        INSERT INTO track VALUES(:song,:sec)
        """, zip(track, sec))
    con.commit()


@app.route("/")
def main():
    return flask.render_template('Main.html')


@app.route("/names/")
def names():
    fakename()
    con = sqlite3.connect("cust.db")
    cur = con.cursor()
    res = cur.execute("SELECT COUNT(DISTINCT name) FROM customers")
    res1 = str(res.fetchall()).replace("(", '').replace(")", '').replace("[", '').replace("]", '').replace(',', '')
    return flask.render_template('Name.html', requirements=res1 + " have unical name")


@app.route("/tracks/")
def tracks():
    faketrack()
    con = sqlite3.connect("track.db")
    cur = con.cursor()
    res = cur.execute("SELECT COUNT(song) FROM track")
    res2 = str(res.fetchall()).replace("(", '').replace(")", '').replace("[", '').replace("]", '').replace(',', '')
    return flask.render_template('Track.html', requirements=res2 + " tracks")


@app.route("/tracks-sec/")
def track_sec():
    faketrack()
    con = sqlite3.connect("track.db")
    cur = con.cursor()
    res = cur.execute("SELECT song,sec FROM track")
    res3 = res.fetchall()
    res5 = []
    for res4 in res3:
        res5.append(str(res4).replace("(", '').replace(")", '').replace(",", '').replace("'", '') + " " + "sec")

    return flask.render_template('Track and sec.html', requirements=res5)


@app.errorhandler(404)
def page_not_found(error):
    return 'Sorry,page not found', 404


if __name__ == "__main__":
    app.run()

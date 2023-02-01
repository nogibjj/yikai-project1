from flask import Flask, render_template, redirect, url_for, request, session
from scrape import scrape
import flask

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import newscrawler
import hashlib
import uuid


@newscrawler.app.route("/")
def index():
  if ('current' in session):
    context = {"username": session["current"]}
    return render_template("index.html", **context)
  return redirect(url_for("login"))


@newscrawler.app.route("/portfolio/")
def portfolio():
  if ('current' in session):
    connection = newscrawler.get_db()
    name = session["current"]
    cur0 = connection.execute(
      "SELECT companyname, active FROM companies WHERE owner = '" + name + "'"
    )
    companies = []
    for item in cur0.fetchall():
      company = {}
      company["companyname"] = item[0]
      company["active"] = item[1]
      companies.append(company)
    context = {"companies": companies}
    return render_template("portfolio.html", **context)
  return redirect(url_for("login"))

@newscrawler.app.route("/sources/")
def sources():
  if ('current' in session):
    connection = newscrawler.get_db()
    name = session["current"]
    cur0 = connection.execute(
      "SELECT sourcename, active FROM sources WHERE owner = '" + name + "'"
    )
    sources = []
    for item in cur0.fetchall():
      source = {}
      source["sourcename"] = item[0]
      source["active"] = item[1]
      sources.append(source)
    context = {"sources": sources}
    return render_template("sources.html", **context)
  return redirect(url_for("login"))

@newscrawler.app.route("/crawl/")
def crawl():
  if 'current' in session:
    connection = newscrawler.get_db()
    name = session["current"]
    cur0 = connection.execute(
      "SELECT companyname FROM companies WHERE owner = '" + name + "' AND active = 1" 
    )
    cur1 = connection.execute(
     "SELECT sourcename FROM sources WHERE owner = '" + name + "' AND active = 1"
    )
    sources,companies = [],[]
    curl2 = connection.execute(
      "SELECT numnews FROM users WHERE username = '" + name + "'"
    )
    number = curl2.fetchall()[0][0]
    curl3 = connection.execute(
      "SELECT groupbysource FROM users WHERE username = '" + name + "'"
    )
    groupbysource = curl3.fetchall()[0][0]
    for item in cur1.fetchall():
      sources.append(item[0])
    for item in cur0.fetchall():
      companies.append(item[0])
    news = scrape(sources, companies, number, groupbysource)
    context = {"news":news}
    return render_template("crawl.html", **context)
  return redirect(url_for("login"))


@newscrawler.app.route("/login/", methods=['POST', 'GET'])
def login():
  if 'current' in session:
    return redirect(url_for('index'))
  if request.method == 'POST':  # not in session
    connection = newscrawler.get_db()
    name = request.form["username"]
    password = request.form["password"]
    cur0 = connection.execute(
      "SELECT EXISTS(SELECT password FROM users WHERE users.username = '" + name + "') AS count"
    )
    count = cur0.fetchall()[0][0]
    if count == 1:  # if user exist
      cur = connection.execute(
        "SELECT password FROM users WHERE users.username = '"
        + name + "'"
      )
      check = cur.fetchall()[0][0]
      algorithm = 'sha512'
      salt = check[7:39]  # grab salt from stored password
      hash_obj = hashlib.new(algorithm)
      password_salted = salt + password
      hash_obj.update(password_salted.encode('utf-8'))
      password_hash = hash_obj.hexdigest()
      password_db_string = "$".join([algorithm, salt, password_hash])
      # if check == password:
      if password_db_string == check:  # check for password
        session["current"] = name
        return redirect(url_for("index"))
      return flask.abort(403)  # wrong password
    return flask.abort(403)  # user does not exist
  return render_template("login.html")

@newscrawler.app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session.pop('current', None)
    return redirect(url_for('login'))

@newscrawler.app.route("/signup/", methods=['POST', 'GET'])
def signup():
  if request.method == 'POST':
    connection = newscrawler.get_db()
    username = request.form["username"]
    password = request.form["password"]
    cur0 = connection.execute(
        "SELECT EXISTS(SELECT * FROM users WHERE users.username = '"
        + username + "') AS count"
    )
    if cur0.fetchall()[0][0] == 1:  # if the user already exist
        return flask.abort(409)
    if len(password) == 0:  # if password is empty
        return flask.abort(400)
    # store user into database
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    p_db_string = "$".join([algorithm, salt, password_hash])
    connection.execute(
        "INSERT INTO users(username, password) VALUES('" + username + "', '" + p_db_string + "')"
    )
    connection.execute(
        "INSERT INTO sources(sourcename, owner, active) "
        + "VALUES('BBC News', '" + username + "', 1), "
        + "('Chicago Tribune', '" + username + "', 1), "
        + "('Forbes', '" + username + "', 1), "
        + "('Investopedia', '" + username + "', 1), "   
        + "('TheStreet', '" + username + "', 1), "
        + "('The Economist', '" + username + "', 1), "
        + "('The New Yorker', '" + username + "', 1), "
        + "('The New York Times', '" + username + "', 1), "
        # + "('The Wall Street Journal', '" + username + "', 1), "
        + "('USA TODAY', '" + username + "', 1)"
    )
    session["current"] = username
    return redirect(url_for('index'))
  return render_template("signup.html")


# api

@newscrawler.app.route('/api/portfolio/', methods=["GET"])
def get_company():
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        cur = connection.execute("SELECT companyname, active FROM companies WHERE owner= '" + logname + "'")
        companies = cur.fetchall()
        portfolio = []
        for company in companies:
            active = {}
            active["companyname"] = company[0]
            active["active"] = company[1]
            portfolio.append(active)
        context = {}
        context["companies"] = portfolio
        return flask.jsonify(**context)

    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403


@newscrawler.app.route('/api/portfolio/<companyname>/', methods=["GET", "POST", "DELETE"])
def post_delete_company(companyname):
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        check_cur = connection.execute(
          "SELECT * FROM companies "
          "WHERE owner=? AND companyname=?",
          (logname, companyname)
        )
        check = check_cur.fetchone()

        if flask.request.method == "DELETE":
            if check is None or len(check) == 0:
              context = {
              "message": "NOT FOUND",
              "status_code": 404
              }
              return flask.jsonify(**context), 404

            connection.execute(
              "DELETE FROM companies WHERE owner=? AND companyname=?",
              (logname, companyname)
            )
            return flask.jsonify({}), 204

        if flask.request.method == "POST":
            if check is None or len(check) == 0:
                connection.execute(
                    "INSERT INTO companies(owner,companyname,active) VALUES (?,?,?)",
                    (logname, companyname, 1)
                )
                content = {
                  "active": 1,
                  "companyname": companyname
                }
                return flask.jsonify(**content), 201
            context = {
                "logname": logname,
                "message": "Conflict",
                "companyname": companyname,
                "status": 409
            }
            return flask.jsonify(**context), 409
        
    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

@newscrawler.app.route('/api/sources/', methods=["GET"])
def get_sources():
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        cur = connection.execute("SELECT sourcename, active FROM sources WHERE owner= '" + logname + "'",
            )
        sources = cur.fetchall()
        temp = []
        for source in sources:
          active = {}
          active["sourcename"] = source[0]
          active["active"] = source[1]
          temp.append(active)
        context = {}
        context["sources"] = temp
        return flask.jsonify(**context)

    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

@newscrawler.app.route('/api/sources/<sourcename>/', methods=["GET","PUT"])
def update_source(sourcename):
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        check_cur = connection.execute(
                      "SELECT active FROM sources "
                      "WHERE owner=? AND sourcename=?",
                      (logname, sourcename)
                    )
        check = check_cur.fetchone()
        if check is None or len(check) == 0:
          context = {
                "message": "NOT FOUND",
                "status_code": 404
                }
          return flask.jsonify(**context), 404
        if check[0] == 0:
          check = str(1)
        else:
          check = str(0)
        connection.execute("UPDATE sources SET active = " + check + " WHERE owner= '" + logname + "' " + "AND sourcename= '" + sourcename + "'",
            )
        context = {"logname": logname,
                   "sourcename": sourcename,
                   "active": check
        }
        return flask.jsonify(**context)
    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

@newscrawler.app.route('/api/sources/<int:temp>/', methods=["GET","PUT"])
def update_num_news(temp):
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        connection.execute("UPDATE users SET numnews = " + str(temp) + " WHERE username= '" + logname + "' ",
            )
        context = {"logname": logname,
                   "numnews": temp,
        }
        return flask.jsonify(**context)
    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

@newscrawler.app.route('/api/portfolio/<companyname>/', methods=["GET","PUT"])
def update_company(companyname):
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        check_cur = connection.execute(
                      "SELECT active FROM companies "
                      "WHERE owner=? AND companyname=?",
                      (logname, companyname)
                    )
        check = check_cur.fetchone()
        if check is None or len(check) == 0:
          context = {
                "message": "NOT FOUND",
                "status_code": 404
                }
          return flask.jsonify(**context), 404
        if check[0] == 0:
          check = str(1)
        else:
          check = str(0)
        connection.execute("UPDATE companies SET active = " + check + " WHERE owner= '" + logname + "' " + "AND companyname= '" + companyname + "'",
            )
        context = {"logname": logname,
                   "companyname": companyname,
                   "active": check
        }
        return flask.jsonify(**context)
    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

@newscrawler.app.route('/api/numnews/', methods=["GET"])
def get_numnews():
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        cur = connection.execute("SELECT numnews FROM users WHERE username= '" + logname + "'",
            )
        numnews = cur.fetchone()[0]
        context = {}
        context["numnews"] = numnews
        cur = connection.execute("SELECT groupbysource FROM users WHERE username= '" + logname + "'",
            )
        groupby = cur.fetchone()[0]
        context["groupby"] = groupby
        return flask.jsonify(**context)

    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

@newscrawler.app.route('/api/sources/groupby/<int:temp>/', methods=["GET","PUT"])
def update_group_by(temp):
    if 'current' in session:
        logname = session['current']
        connection = newscrawler.get_db()
        connection.execute("UPDATE users SET groupbysource = " + str(temp) + " WHERE username= '" + logname + "' ",
            )
        context = {"logname": logname,
                   "groupbysource": temp,
        }
        return flask.jsonify(**context)
    forbidden_error = {
        "message": "Forbidden",
        "status_code": 403
    }
    return flask.jsonify(**forbidden_error), 403

if __name__ == "__main__":
  newscrawler.app.run()
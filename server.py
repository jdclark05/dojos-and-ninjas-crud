from flask import Flask,render_template,redirect,request
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)

@app.route('/')
def index():
    query = "SELECT * FROM dojos;"
    dojos = connectToMySQL('dojos-and-ninjas').query_db(query)
    return render_template("index.html",dojos=dojos)
    

@app.route('/', methods=["POST"])
def add_dojo():
    if request.form:
        query = "INSERT INTO dojos (name) VALUES (%(name)s)"
        data = {
            "name":request.form['name']
        }
        dojos = connectToMySQL('dojos-and-ninjas').query_db(query, data)
        return redirect("/")
    else:
        return redirect("index.html")

@app.route('/create_ninja', methods=["POST", "GET"])
def add_ninja():
    if request.form:
        query = "INSERT INTO ninjas (first_name, last_name, age, dojo_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s)"
        dojo_id = request.form['dojo_id']
        data = {
            "first_name":request.form['first_name'],
            "last_name":request.form['last_name'],
            "age":request.form['age'],
            "dojo_id":dojo_id
        }
        ninjas = connectToMySQL('dojos-and-ninjas').query_db(query, data)
        return redirect(f"/dojo_show/{dojo_id}")
    else:
        query = "SELECT * FROM dojos;"
        dojos =  connectToMySQL('dojos-and-ninjas').query_db(query)
        return render_template("create_ninja.html", dojos=dojos)


@app.route('/dojo_show/<int:dojo_id>', methods=['GET'])
def dojo_show(dojo_id):
        query = "SELECT ninjas.first_name, ninjas.last_name, ninjas.age, dojos.name FROM ninjas JOIN dojos ON dojos.id = ninjas.dojo_id WHERE dojos.id=%(dojo_id)s"
        data = {
            "dojo_id":dojo_id
        }
        ninjas = connectToMySQL('dojos-and-ninjas').query_db(query, data)
        print(ninjas)
        return render_template(f"dojo_show.html", ninjas=ninjas)


if __name__ == "__main__":
    app.run(debug=True)
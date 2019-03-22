from flask import Flask, jsonify, render_template, request
import requests
import json

app = Flask(__name__)

app.config["DEBUG"] = True 

@app.route('/')
@app.route("/search", methods=["GET", "POST"])
def search():
	if request.method == "POST":
		url = "https://images-api.nasa.gov/search?media_type=image&q=" + request.form["user_search"] + "&location=" + request.form["location"]
		if request.form["start_year"]:
			url += "&year_start=" + request.form["start_year"]
		if request.form["end_year"]:
			url += "&year_end=" + request.form["end_year"]
		response_dict = requests.get(url).json()
		
		#return jsonify(response_dict)
		if (response_dict["collection"]["metadata"]["total_hits"] == 0):
			return render_template("notfound.html")
		else:
			return render_template("results.html", api_data=response_dict)
	else:
		return render_template("index.html")

@app.route('/image/<id>')
def image(id):
	url = "https://images-api.nasa.gov/search?media_type=image&nasa_id=" + id
	response_dict = requests.get(url).json()
	#return jsonify(response_dict)
	if (response_dict["collection"]["metadata"]["total_hits"] == 0):
		return render_template("notfound.html")
	else:
		return render_template("image.html", api_data=response_dict)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
	

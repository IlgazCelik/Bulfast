from model import findClosestNeighbors
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

vectorSize = 512



#Search function
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json() or {}
    vectorStn = [0.0] * vectorSize
    user_vector = data.get("vector", vectorStn)
    threshold = data.get("threshold", 0.1)

    matched_indices = findClosestNeighbors(user_vector, DATABASE, threshold)

    return jsonify({"success": True, "matchesIdx": matched_indices})


if __name__ == "__main__":
    app.run(debug=True)


#To do
#Integrate database operations
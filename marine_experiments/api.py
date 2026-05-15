"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from database_functions import get_db_connection, get_experiment, delete_experiment


app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection. 

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })


@app.get("/experiment")
def endpoint_get_experiment():
    """Returns experiments with optional filtering."""

    exp_type = request.args.get("type")
    score_over = request.args.get("score_over")

    valid_types = {"intelligence", "obedience", "aggression"}

    if exp_type is not None:
        if exp_type.lower() not in valid_types:
            return {"error": "Invalid value for 'type' parameter"}, 400

    if score_over is not None:
        if not score_over.isdigit():
            return {"error": "Invalid value for 'score_over' parameter"}, 400

    score_over = int(score_over)

    if score_over < 0 or score_over > 100:
        return {"error": "Invalid value for 'score_over' parameter"}, 400

    if exp_type:
        exp_type = exp_type.lower()

    experiments = get_experiment(
        conn,
        exp_type,
        score_over
    )

    return jsonify(experiments), 200


@app.delete("/experiment/<int:experiment_id>")
def endpoint_delete_experiment(experiment_id):
    """Deletes a specific experiment."""

    experiment = delete_experiment(conn, experiment_id)

    if not experiment:
        return jsonify({
            "error": f"Unable to locate experiment with ID {experiment_id}."
        }), 404

    return jsonify(experiment), 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()

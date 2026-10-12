
from flask import Flask, render_template, request, jsonify

from analyzer import analyze_password
from security_checks import validate_password, detect_security_risks
import database

app = Flask(__name__)

# Initialize the database when the application starts.
database.initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # Read the JSON request safely.
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a valid JSON request."
        }), 400

    password = data.get("password", "")

    # Validate the password type.
    if not isinstance(password, str):
        return jsonify({
            "error": "Password must be text."
        }), 400

    # Reject empty passwords before database operations.
    if not password:
        return jsonify({
            "error": "Enter a password to analyze."
        }), 400

    # Validate password length and other input constraints.
    validation = validate_password(password)

    if not validation["valid"]:
        return jsonify({
            "error": validation["error"]
        }), 400

    try:
        # Analyze password strength.
        result = analyze_password(password)

        # Detect additional security risks.
        result["security_risks"] = detect_security_risks(password)

        # Save metadata only, never the password itself.
        database.save_analysis(result)

        # Return the analysis report to the frontend.
        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400


@app.route("/history")
def history():
    # Retrieve the latest 50 analysis records.
    records = database.get_analysis_history(limit=50)

    return render_template(
        "history.html",
        history=records
    )


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "The requested page was not found."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": "An internal server error occurred."
    }), 500


if __name__ == "__main__":
    # Debug mode is intended for local development only.
    app.run(debug=True)

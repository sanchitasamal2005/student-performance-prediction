from flask import Flask, render_template, request, jsonify, send_file, Response
import joblib
import pandas as pd
import sqlite3
from datetime import datetime


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

app = Flask(__name__)


# ==========================================
# LOAD ML MODEL
# ==========================================

model = joblib.load(
    "model/student_performance_pipeline.pkl"
)

print("ML model loaded successfully!")


# ==========================================
# DATABASE
# ==========================================

def create_database():

    connection = sqlite3.connect("predictions.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date_time TEXT,

            hours_studied REAL,

            attendance REAL,

            previous_scores REAL,

            tutoring_sessions REAL,

            sleep_hours REAL,

            physical_activity REAL,

            predicted_score REAL,

            performance TEXT

        )
    """)

    connection.commit()
    connection.close()


create_database()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# PREDICTION
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # Convert input into DataFrame
        input_data = pd.DataFrame([data])

        # ML prediction
        prediction = model.predict(input_data)[0]

        prediction = max(
            0,
            min(100, prediction)
        )

        prediction = round(
            float(prediction),
            2
        )


        # ==================================
        # PERFORMANCE LEVEL
        # ==================================

        if prediction >= 90:

            performance = "Excellent"

        elif prediction >= 75:

            performance = "Very Good"

        elif prediction >= 60:

            performance = "Good"

        elif prediction >= 40:

            performance = "Average"

        else:

            performance = "Needs Improvement"


        # ==================================
        # SAVE TO DATABASE
        # ==================================

        connection = sqlite3.connect(
            "predictions.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO predictions
            (
                date_time,
                hours_studied,
                attendance,
                previous_scores,
                tutoring_sessions,
                sleep_hours,
                physical_activity,
                predicted_score,
                performance
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),

            data["Hours_Studied"],

            data["Attendance"],

            data["Previous_Scores"],

            data["Tutoring_Sessions"],

            data["Sleep_Hours"],

            data["Physical_Activity"],

            prediction,

            performance

        ))

        connection.commit()
        connection.close()


        return jsonify({

            "success": True,

            "prediction": prediction,

            "performance": performance

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ==========================================
# HISTORY PAGE
# ==========================================
# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    connection = sqlite3.connect(
        "predictions.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    connection.close()


    # ==================================
    # DASHBOARD STATISTICS
    # ==================================

    total_predictions = len(predictions)

    if total_predictions > 0:

        scores = [
            row["predicted_score"]
            for row in predictions
        ]

        average_score = round(
            sum(scores) / len(scores),
            2
        )

        highest_score = round(
            max(scores),
            2
        )

    else:

        average_score = 0
        highest_score = 0


    return render_template(
        "dashboard.html",
        predictions=predictions,
        total_predictions=total_predictions,
        average_score=average_score,
        highest_score=highest_score
    )
@app.route("/history")
def history():

    connection = sqlite3.connect(
        "predictions.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        predictions=predictions
    )


# ==========================================
# RUN APPLICATION
# ==========================================
# MODEL PERFORMANCE PAGE
@app.route("/model-performance")
def model_performance():

    try:

        model_results = pd.read_csv(
            "model/model_comparison.csv"
        )

        models = model_results.to_dict(
            orient="records"
        )

        # Find model with lowest MAE
        best_model_row = model_results.loc[
            model_results["MAE"].idxmin()
        ]

        best_model = best_model_row["Model"]
        best_mae = best_model_row["MAE"]
        best_rmse = best_model_row["RMSE"]
        best_r2 = best_model_row["R2"]

    except Exception:

        models = []

        best_model = "Not Available"
        best_mae = "-"
        best_rmse = "-"
        best_r2 = "-"

    return render_template(
        "model_performance.html",
        models=models,
        best_model=best_model,
        best_mae=best_mae,
        best_rmse=best_rmse,
        best_r2=best_r2
    )

    try:

        model_results = pd.read_csv(
            "model/model_comparison.csv"
        )

        models = model_results.to_dict(
            orient="records"
        )

    except Exception:

        models = []

    return render_template(
        "model_performance.html",
        models=models
    )
    
    # =========================================
# PDF PREDICTION REPORT
# =========================================

@app.route("/download-report", methods=["POST"])
def download_report():

    try:

        data = request.get_json()

        score = float(data["prediction"])
        performance = data["performance"]

        hours_studied = data["Hours_Studied"]
        attendance = data["Attendance"]
        previous_scores = data["Previous_Scores"]
        tutoring_sessions = data["Tutoring_Sessions"]

        sleep_hours = data["Sleep_Hours"]
        physical_activity = data["Physical_Activity"]

        report_path = "student_prediction_report.pdf"

        pdf = canvas.Canvas(
            report_path,
            pagesize=A4
        )

        width, height = A4

        # =================================
        # TITLE
        # =================================

        pdf.setFillColor(colors.HexColor("#4f46e5"))

        pdf.setFont(
            "Helvetica-Bold",
            24
        )

        pdf.drawCentredString(
            width / 2,
            height - 70,
            "Student Performance Prediction"
        )

        # =================================
        # SUBTITLE
        # =================================

        pdf.setFillColor(colors.black)

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawCentredString(
            width / 2,
            height - 95,
            "Machine Learning Prediction Report"
        )

        # =================================
        # LINE
        # =================================

        pdf.setStrokeColor(
            colors.HexColor("#4f46e5")
        )

        pdf.line(
            50,
            height - 115,
            width - 50,
            height - 115
        )

        # =================================
        # PREDICTION RESULT
        # =================================

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            60,
            height - 160,
            "Prediction Result"
        )

        pdf.setFont(
            "Helvetica",
            14
        )

        pdf.drawString(
            60,
            height - 195,
            f"Predicted Exam Score: {score} / 100"
        )

        pdf.drawString(
            60,
            height - 225,
            f"Performance Level: {performance}"
        )

        # =================================
        # INPUT DETAILS
        # =================================

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            60,
            height - 275,
            "Student Input Summary"
        )

        pdf.setFont(
            "Helvetica",
            13
        )

        details = [

            f"Hours Studied: {hours_studied}",

            f"Attendance: {attendance}%",

            f"Previous Score: {previous_scores}",

            f"Tutoring Sessions: {tutoring_sessions}",

            f"Sleep Hours: {sleep_hours}",

            f"Physical Activity: {physical_activity}"

        ]

        y_position = height - 310

        for detail in details:

            pdf.drawString(
                70,
                y_position,
                detail
            )

            y_position -= 28

        # =================================
        # NOTE
        # =================================

        pdf.setFont(
            "Helvetica-Bold",
            15
        )

        pdf.drawString(
            60,
            y_position - 20,
            "Important Note"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        note = (
            "The predicted score is an estimate generated "
            "by a machine learning model. It should not be "
            "considered an exact future exam result."
        )

        # Wrap the note manually
        pdf.drawString(
            60,
            y_position - 45,
            note[:95]
        )

        pdf.drawString(
            60,
            y_position - 62,
            note[95:]
        )

        # =================================
        # DATE
        # =================================

        pdf.setFont(
            "Helvetica",
            10
        )

        current_date = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        pdf.drawString(
            60,
            50,
            f"Generated on: {current_date}"
        )

        # =================================
        # FOOTER
        # =================================

        pdf.drawRightString(
            width - 60,
            50,
            "Student Performance Prediction"
        )

        pdf.save()

        return send_file(
            report_path,
            as_attachment=True,
            download_name="student_prediction_report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
     # =========================================
# EXPORT PREDICTION HISTORY AS CSV
# =========================================

@app.route("/export-csv")
def export_csv():

    try:

        connection = sqlite3.connect(
            "predictions.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                date_time,
                hours_studied,
                attendance,
                previous_scores,
                tutoring_sessions,
                sleep_hours,
                physical_activity,
                predicted_score,
                performance
            FROM predictions
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        connection.close()


        # CSV HEADER

        csv_data = (
            "Date & Time,"
            "Hours Studied,"
            "Attendance,"
            "Previous Score,"
            "Tutoring Sessions,"
            "Sleep Hours,"
            "Physical Activity,"
            "Predicted Score,"
            "Performance\n"
        )


        # CSV ROWS

        for row in rows:

            csv_data += ",".join(
                str(value)
                for value in row
            )

            csv_data += "\n"


        return Response(

            csv_data,

            mimetype="text/csv",

            headers={
                "Content-Disposition":
                "attachment; filename=prediction_history.csv"
            }

        )


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400   
        
if __name__ == "__main__":

    app.run(debug=True)
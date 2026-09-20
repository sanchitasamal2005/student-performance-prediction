// =============================
// STUDENT PERFORMANCE PREDICTION
// =============================


// =================================
// PREDICTION FORM
// =================================

const predictionForm =
    document.getElementById("predictionForm");


if (predictionForm) {

    predictionForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const form = event.target;

            const predictButton =
                document.getElementById(
                    "predictButton"
                );


            // =================================
            // GET VALUES
            // =================================

            const hoursStudied =
                Number(form.Hours_Studied.value);

            const attendance =
                Number(form.Attendance.value);

            const previousScores =
                Number(form.Previous_Scores.value);

            const tutoringSessions =
                Number(form.Tutoring_Sessions.value);

            const sleepHours =
                Number(form.Sleep_Hours.value);

            const physicalActivity =
                Number(form.Physical_Activity.value);


            // =================================
            // VALIDATION
            // =================================

            if (
                hoursStudied < 0 ||
                hoursStudied > 24
            ) {

                alert(
                    "Hours Studied must be between 0 and 24."
                );

                return;
            }


            if (
                attendance < 0 ||
                attendance > 100
            ) {

                alert(
                    "Attendance must be between 0 and 100."
                );

                return;
            }


            if (
                previousScores < 0 ||
                previousScores > 100
            ) {

                alert(
                    "Previous Score must be between 0 and 100."
                );

                return;
            }


            if (tutoringSessions < 0) {

                alert(
                    "Tutoring Sessions cannot be negative."
                );

                return;
            }


            if (
                sleepHours < 0 ||
                sleepHours > 24
            ) {

                alert(
                    "Sleep Hours must be between 0 and 24."
                );

                return;
            }


            if (physicalActivity < 0) {

                alert(
                    "Physical Activity cannot be negative."
                );

                return;
            }


            // =================================
            // LOADING
            // =================================

            predictButton.disabled = true;

            predictButton.classList.add(
                "loading"
            );

            predictButton.innerHTML =
                '<span class="loading-spinner"></span> Predicting...';


            // =================================
            // FORM DATA
            // =================================

            const data = {

                Hours_Studied:
                    hoursStudied,

                Attendance:
                    attendance,

                Previous_Scores:
                    previousScores,

                Tutoring_Sessions:
                    tutoringSessions,

                Sleep_Hours:
                    sleepHours,

                Physical_Activity:
                    physicalActivity,

                Parental_Involvement:
                    form.Parental_Involvement.value,

                Access_to_Resources:
                    form.Access_to_Resources.value,

                Extracurricular_Activities:
                    form.Extracurricular_Activities.value,

                Motivation_Level:
                    form.Motivation_Level.value,

                Internet_Access:
                    form.Internet_Access.value,

                Family_Income:
                    form.Family_Income.value,

                Teacher_Quality:
                    form.Teacher_Quality.value,

                School_Type:
                    form.School_Type.value,

                Peer_Influence:
                    form.Peer_Influence.value,

                Learning_Disabilities:
                    form.Learning_Disabilities.value,

                Parental_Education_Level:
                    form.Parental_Education_Level.value,

                Distance_from_Home:
                    form.Distance_from_Home.value,

                Gender:
                    form.Gender.value
            };


            // =================================
            // SEND TO FLASK
            // =================================

            try {

                const response =
                    await fetch(
                        "/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(data)
                        }
                    );


                const result =
                    await response.json();


                // =================================
                // SUCCESS
                // =================================

                if (result.success) {

                    const score =
                        Number(
                            result.prediction
                        );


                    // =================================
                    // SCORE
                    // =================================

                    document
                        .getElementById(
                            "predictionValue"
                        )
                        .textContent =
                        score;


                    // =================================
                    // PERFORMANCE
                    // =================================

                    document
                        .getElementById(
                            "performanceLevel"
                        )
                        .textContent =
                        result.performance;


                    // =================================
                    // INSIGHT
                    // =================================

                    let insight = "";


                    if (score >= 90) {

                        insight =
                            "The predicted score is very high. Continue maintaining consistent study habits and attendance.";

                    }

                    else if (score >= 75) {

                        insight =
                            "The predicted score is strong. Regular revision and consistent preparation can help maintain this level.";

                    }

                    else if (score >= 60) {

                        insight =
                            "The predicted score is in a good range. More focused study and revision may help improve performance.";

                    }

                    else if (score >= 40) {

                        insight =
                            "The predicted score is in the average range. Consider improving study time, attendance, and revision habits.";

                    }

                    else {

                        insight =
                            "The predicted score indicates that additional academic support and consistent study may be helpful.";

                    }


                    document
                        .getElementById(
                            "insightMessage"
                        )
                        .textContent =
                        insight;


                    // =================================
                    // PROGRESS BAR
                    // =================================

                    const progress =
                        document.getElementById(
                            "scoreProgress"
                        );


                    if (progress) {

                        progress.style.width =
                            score + "%";
                    }


                    // =================================
                    // PREDICTION SUMMARY
                    // =================================

                    document
                        .getElementById(
                            "summaryHours"
                        )
                        .textContent =
                        hoursStudied + " hours";


                    document
                        .getElementById(
                            "summaryAttendance"
                        )
                        .textContent =
                        attendance + "%";


                    document
                        .getElementById(
                            "summaryPrevious"
                        )
                        .textContent =
                        previousScores;


                    document
                        .getElementById(
                            "summaryTutoring"
                        )
                        .textContent =
                        tutoringSessions;


                    // =================================
                    // SHOW RESULT
                    // =================================

                    document
                        .getElementById(
                            "result"
                        )
                        .style.display =
                        "block";


                    // =================================
                    // RESET BUTTON
                    // =================================

                    predictButton.disabled =
                        false;

                    predictButton.classList.remove(
                        "loading"
                    );

                    predictButton.innerHTML =
                        "🔮 Predict Exam Score";

                }


                // =================================
                // FLASK ERROR
                // =================================

                else {

                    alert(
                        "Prediction Error: " +
                        result.error
                    );


                    predictButton.disabled =
                        false;

                    predictButton.classList.remove(
                        "loading"
                    );

                    predictButton.innerHTML =
                        "🔮 Predict Exam Score";
                }

            }


            // =================================
            // CONNECTION ERROR
            // =================================

            catch (error) {

                alert(
                    "Something went wrong: " +
                    error
                );


                predictButton.disabled =
                    false;

                predictButton.classList.remove(
                    "loading"
                );

                predictButton.innerHTML =
                    "🔮 Predict Exam Score";
            }

        }
    );

}


// =================================
// DARK / LIGHT MODE
// =================================

const themeToggle =
    document.getElementById(
        "themeToggle"
    );


const savedTheme =
    localStorage.getItem(
        "theme"
    );


if (savedTheme === "dark") {

    document.body.classList.add(
        "dark-mode"
    );

    if (themeToggle) {

        themeToggle.textContent =
            "☀️";
    }
}


if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        function () {

            document.body.classList.toggle(
                "dark-mode"
            );


            if (
                document.body.classList.contains(
                    "dark-mode"
                )
            ) {

                localStorage.setItem(
                    "theme",
                    "dark"
                );

                themeToggle.textContent =
                    "☀️";

            }

            else {

                localStorage.setItem(
                    "theme",
                    "light"
                );

                themeToggle.textContent =
                    "🌙";
            }

        }
    );

}


// =================================
// CLEAR FORM
// =================================

const clearButton =
    document.getElementById(
        "clearButton"
    );


if (clearButton) {

    clearButton.addEventListener(
        "click",
        function () {

            predictionForm.reset();


            const result =
                document.getElementById(
                    "result"
                );


            if (result) {

                result.style.display =
                    "none";
            }


            document
                .getElementById(
                    "predictionValue"
                )
                .textContent =
                "--";


            document
                .getElementById(
                    "performanceLevel"
                )
                .textContent =
                "--";


            document
                .getElementById(
                    "insightMessage"
                )
                .textContent =
                "Your performance insight will appear here.";


            document
                .getElementById(
                    "predictionMessage"
                )
                .textContent =
                "Your prediction has been saved to history.";


            document
                .getElementById(
                    "summaryHours"
                )
                .textContent =
                "--";


            document
                .getElementById(
                    "summaryAttendance"
                )
                .textContent =
                "--";


            document
                .getElementById(
                    "summaryPrevious"
                )
                .textContent =
                "--";


            document
                .getElementById(
                    "summaryTutoring"
                )
                .textContent =
                "--";


            const scoreProgress =
                document.getElementById(
                    "scoreProgress"
                );


            if (scoreProgress) {

                scoreProgress.style.width =
                    "0%";
            }

        }
    );

}

// =================================
// DOWNLOAD PDF REPORT
// =================================

const downloadReportButton =
    document.getElementById(
        "downloadReportButton"
    );


if (downloadReportButton) {

    downloadReportButton.addEventListener(
        "click",
        async function () {

            const predictionValue =
                document.getElementById(
                    "predictionValue"
                ).textContent;


            const performanceLevel =
                document.getElementById(
                    "performanceLevel"
                ).textContent;


            if (
                predictionValue === "--" ||
                performanceLevel === "--"
            ) {

                alert(
                    "Please make a prediction first."
                );

                return;
            }


            const form =
                document.getElementById(
                    "predictionForm"
                );


            const data = {

                prediction:
                    Number(predictionValue),

                performance:
                    performanceLevel,

                Hours_Studied:
                    Number(
                        form.Hours_Studied.value
                    ),

                Attendance:
                    Number(
                        form.Attendance.value
                    ),

                Previous_Scores:
                    Number(
                        form.Previous_Scores.value
                    ),

                Tutoring_Sessions:
                    Number(
                        form.Tutoring_Sessions.value
                    ),

                Sleep_Hours:
                    Number(
                        form.Sleep_Hours.value
                    ),

                Physical_Activity:
                    Number(
                        form.Physical_Activity.value
                    )

            };


            downloadReportButton.disabled =
                true;


            downloadReportButton.textContent =
                "⏳ Generating Report...";


            try {

                const response =
                    await fetch(
                        "/download-report",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(data)
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Could not generate PDF."
                    );

                }


                const blob =
                    await response.blob();


                const url =
                    window.URL.createObjectURL(
                        blob
                    );


                const link =
                    document.createElement(
                        "a"
                    );


                link.href = url;

                link.download =
                    "student_prediction_report.pdf";


                document.body.appendChild(
                    link
                );


                link.click();


                link.remove();


                window.URL.revokeObjectURL(
                    url
                );

            }


            catch (error) {

                alert(
                    "Report generation failed: " +
                    error.message
                );

            }


            finally {

                downloadReportButton.disabled =
                    false;

                downloadReportButton.textContent =
                    "📄 Download Prediction Report";

            }

        }
    );

}
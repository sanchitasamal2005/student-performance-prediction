import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Regression models
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import HistGradientBoostingRegressor

# Evaluation
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# =========================================================
# 1. LOAD DATASET
# =========================================================

print("\n==========================================")
print("LOADING DATASET")
print("==========================================")

df = pd.read_csv("dataset/student_performance.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# =========================================================
# 2. SEPARATE FEATURES AND TARGET
# =========================================================

X = df.drop("Exam_Score", axis=1)
y = df["Exam_Score"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)


# =========================================================
# 3. IDENTIFY COLUMN TYPES
# =========================================================

categorical_features = X.select_dtypes(
    include=["object", "str"]
).columns.tolist()

numeric_features = X.select_dtypes(
    exclude=["object", "str"]
).columns.tolist()

print("\n==========================================")
print("CATEGORICAL FEATURES")
print("==========================================")

print(categorical_features)

print("\n==========================================")
print("NUMERIC FEATURES")
print("==========================================")

print(numeric_features)


# =========================================================
# 4. SPLIT DATA BEFORE PREPROCESSING
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\n==========================================")
print("DATA SPLIT")
print("==========================================")

print("Training data:", X_train.shape)
print("Testing data :", X_test.shape)


# =========================================================
# 5. CREATE PREPROCESSOR
# =========================================================

# Numeric preprocessing
numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)


# Categorical preprocessing
categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


# Combine both
def create_preprocessor():

    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_transformer,
                numeric_features
            ),
            (
                "categorical",
                categorical_transformer,
                categorical_features
            )
        ]
    )


# =========================================================
# 6. CREATE MODELS
# =========================================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Ridge Regression":
        Ridge(alpha=1.0),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.03,
            max_depth=3,
            random_state=42
        ),

    "Extra Trees":
        ExtraTreesRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        ),

    "Hist Gradient Boosting":
        HistGradientBoostingRegressor(
            max_iter=300,
            learning_rate=0.05,
            max_leaf_nodes=31,
            random_state=42
        )
}


# =========================================================
# 7. TRAIN ALL MODELS
# =========================================================

results = {}
trained_pipelines = {}


print("\n==========================================")
print("MODEL TRAINING")
print("==========================================")


for model_name, model in models.items():

    print("\nTraining:", model_name)

    # Create a NEW preprocessor for every model
    preprocessor = create_preprocessor()

    # Create complete pipeline
    pipeline = Pipeline(
        steps=[
            (
                "preprocessing",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    # Train
    pipeline.fit(
        X_train,
        y_train
    )

    # Predict
    predictions = pipeline.predict(
        X_test
    )

    # Calculate metrics
    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    # Store results
    results[model_name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    trained_pipelines[model_name] = pipeline


# =========================================================
# 8. DISPLAY MODEL COMPARISON
# =========================================================

print("\n")
print("==========================================")
print("MODEL COMPARISON")
print("==========================================")

for model_name, metrics in results.items():

    print("\nModel:", model_name)

    print(
        "MAE :",
        round(metrics["MAE"], 4)
    )

    print(
        "RMSE:",
        round(metrics["RMSE"], 4)
    )

    print(
        "R²  :",
        round(metrics["R2"], 4)
    )


# =========================================================
# 9. FIND BEST MODEL
# =========================================================

# Lower MAE = better prediction
best_model_name = min(
    results,
    key=lambda model_name: results[model_name]["MAE"]
)

best_pipeline = trained_pipelines[
    best_model_name
]

best_metrics = results[
    best_model_name
]


# =========================================================
# 10. DISPLAY BEST MODEL
# =========================================================

print("\n")
print("==========================================")
print("BEST MODEL")
print("==========================================")

print(
    "Selected Model:",
    best_model_name
)

print(
    "Best MAE :",
    round(best_metrics["MAE"], 4)
)

print(
    "Best RMSE:",
    round(best_metrics["RMSE"], 4)
)

print(
    "Best R²  :",
    round(best_metrics["R2"], 4)
)


# =========================================================
# 11. CREATE MODEL FOLDER
# =========================================================

os.makedirs(
    "model",
    exist_ok=True
)


# =========================================================
# 12. SAVE BEST PIPELINE
# =========================================================

model_path = (
    "model/student_performance_pipeline.pkl"
)

joblib.dump(
    best_pipeline,
    model_path
)

print("\n==========================================")
print("MODEL SAVED")
print("==========================================")

print(
    "Saved location:",
    model_path
)


# =========================================================
# 13. SAVE MODEL COMPARISON
# =========================================================

comparison_data = []

for model_name, metrics in results.items():

    comparison_data.append({
        "Model": model_name,
        "MAE": round(metrics["MAE"], 4),
        "RMSE": round(metrics["RMSE"], 4),
        "R2": round(metrics["R2"], 4)
    })


comparison_df = pd.DataFrame(
    comparison_data
)

comparison_path = (
    "model/model_comparison.csv"
)

comparison_df.to_csv(
    comparison_path,
    index=False
)


# =========================================================
# 14. FINAL MESSAGE
# =========================================================

print("\n==========================================")
print("TRAINING COMPLETED SUCCESSFULLY!")
print("==========================================")

print(
    "\nBest model:",
    best_model_name
)

print(
    "Model file:",
    model_path
)

print(
    "Comparison file:",
    comparison_path
)

print("\nYour ML model is ready for Flask!")
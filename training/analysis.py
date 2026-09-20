import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/student_performance.csv")

print("\n==============================")
print("FIRST 5 ROWS")
print("==============================")
print(df.head())


print("\n==============================")
print("NUMBER OF ROWS AND COLUMNS")
print("==============================")
print(df.shape)


print("\n==============================")
print("COLUMN NAMES")
print("==============================")
print(df.columns.tolist())


print("\n==============================")
print("DATA TYPES")
print("==============================")
print(df.dtypes)


print("\n==============================")
print("MISSING VALUES")
print("==============================")
print(df.isnull().sum())


print("\n==============================")
print("DUPLICATE ROWS")
print("==============================")
print(df.duplicated().sum())


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

categorical_columns = [
    "Teacher_Quality",
    "Parental_Education_Level",
    "Distance_from_Home"
]

for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

print("\n==============================")
print("MISSING VALUES AFTER CLEANING")
print("==============================")
print(df.isnull().sum())
import pandas as pd
import numpy as np
import os
import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# CONFIG
DATA_DIR = r"D:\Project\machinehealth_3.O"
FILE_PATTERN = "machine_health_minute_2024_month_*.csv"
TARGET_COL = "MachineHealth"
MODEL_SAVE_DIR = DATA_DIR  # Save models & CSVs in same dir

# Timeframes and their human-readable names
TIMEFRAMES = {
    "H": "Hourly",
    "W": "Weekly",
    "M": "Monthly",
    "Y": "Yearly"
}

# Resample frequency mapping
FREQ_MAP = {
    "H": "H",     # Hourly
    "W": "W",     # Weekly
    "M": "ME",    # Month end
    "Y": "YE",    # Year end
}

def load_data():
    files = sorted(glob.glob(os.path.join(DATA_DIR, FILE_PATTERN)))
    if not files:
        raise ValueError(f"No files found in {DATA_DIR} with pattern {FILE_PATTERN}")
    all_dfs = [pd.read_csv(file) for file in files]
    return pd.concat(all_dfs, ignore_index=True)

def preprocess(df):
    df.columns = [col.replace("Â", "").strip() for col in df.columns]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.sort_values("Timestamp", inplace=True)
    df = df.dropna(subset=[TARGET_COL])
    return df

def aggregate(df, freq_code):
    freq_corrected = FREQ_MAP.get(freq_code, freq_code)
    df = df.copy()
    df.set_index("Timestamp", inplace=True)

    agg = df.resample(freq_corrected).agg({
        "Temperature(°C)": ["mean", "max", "min", "std"],
        "Humidity(%)": ["mean", "max", "min", "std"],
        "SoundLevel(dB)": ["mean", "max", "min", "std"],
        TARGET_COL: lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
    })

    agg.columns = ['_'.join(col).strip() for col in agg.columns.values]
    agg.reset_index(inplace=True)
    return agg

def train_model(agg_df, label_encoder=None):
    agg_df = agg_df.dropna()
    target_col = f"{TARGET_COL}_<lambda>"

    if label_encoder is None:
        label_encoder = LabelEncoder()
        agg_df['Label'] = label_encoder.fit_transform(agg_df[target_col])
    else:
        agg_df['Label'] = label_encoder.transform(agg_df[target_col])

    X = agg_df.drop(columns=["Timestamp", target_col, "Label"])
    y = agg_df["Label"]
    X.fillna(0, inplace=True)

    if len(agg_df) < 2:
        print(f"Warning: Only {len(agg_df)} sample(s). Training on all data without splitting.")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model, label_encoder

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model, label_encoder

def save_model(model, label_encoder, freq_name):
    model_filename = os.path.join(MODEL_SAVE_DIR, f"rf_model_{freq_name.lower()}.joblib")
    encoder_filename = os.path.join(MODEL_SAVE_DIR, f"label_encoder_{freq_name.lower()}.joblib")
    joblib.dump(model, model_filename)
    joblib.dump(label_encoder, encoder_filename)
    print(f"Saved model to {model_filename}")
    print(f"Saved label encoder to {encoder_filename}")

def save_aggregated_data(agg_df, freq_code):
    csv_filename = os.path.join(MODEL_SAVE_DIR, f"aggregated_{freq_code}.csv")
    agg_df.to_csv(csv_filename, index=False)
    print(f"Saved aggregated CSV to {csv_filename}")

def main():
    print("Loading data...")
    df = load_data()
    print("Preprocessing data...")
    df = preprocess(df)

    for freq_code, freq_name in TIMEFRAMES.items():
        print(f"\n=== Aggregating data by {freq_name} ===")
        agg_df = aggregate(df, freq_code)
        save_aggregated_data(agg_df, freq_code)

        target_col = f"{TARGET_COL}_<lambda>"
        if agg_df.empty or target_col not in agg_df.columns:
            print(f"Skipping training for {freq_name}: Missing target column or empty data.")
            continue

        unique_classes = agg_df[target_col].nunique()
        if unique_classes <= 1:
            print(f"Warning: Only one class ('{agg_df[target_col].iloc[0]}') found in target for {freq_name}. Training anyway.")

        print(f"Training model for {freq_name} data...")
        try:
            model, le = train_model(agg_df)
            save_model(model, le, freq_name)
        except Exception as e:
            print(f"Failed to train/save model for {freq_name}: {e}")

if __name__ == "__main__":
    main()

import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report
)

# Create models folder automatically
os.makedirs("models", exist_ok=True)

print("Loading NSL-KDD dataset...")



# Standard NSL-KDD column names
columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted",
    "num_root", "num_file_creations", "num_shells", "num_access_files",
    "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
    "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
    "attack", "difficulty"
]

# Load datasets
train = pd.read_csv("data/KDDTrain+.txt", names=columns)
test = pd.read_csv("data/KDDTest+.txt", names=columns)

print("Datasets loaded successfully!")

# Convert attacks to binary labels
train["attack"] = train["attack"].apply(lambda x: "normal" if x == "normal" else "attack")
test["attack"] = test["attack"].apply(lambda x: "normal" if x == "normal" else "attack")

# Encode categorical features
categorical = ["protocol_type", "service", "flag"]

encoders = {}

for col in categorical:
    le = LabelEncoder()

    combined = pd.concat([train[col], test[col]])
    le.fit(combined)

    train[col] = le.transform(train[col])
    test[col] = le.transform(test[col])

    encoders[col] = le

# Encode target
target_encoder = LabelEncoder()

combined_target = pd.concat([train["attack"], test["attack"]])
target_encoder.fit(combined_target)

train["attack"] = target_encoder.transform(train["attack"])
test["attack"] = target_encoder.transform(test["attack"])

# Remove difficulty column
train.drop("difficulty", axis=1, inplace=True)
test.drop("difficulty", axis=1, inplace=True)

# Split features and labels
X_train = train.drop("attack", axis=1)
y_train = train["attack"]

X_test = test.drop("attack", axis=1)
y_test = test["attack"]

print("Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training complete!")

# Predictions
predictions = model.predict(X_test)

print("\n===== RESULTS =====")
print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")
print(f"Precision: {precision_score(y_test, predictions):.4f}")
print(f"Recall   : {recall_score(y_test, predictions):.4f}")

print("\nClassification Report:\n")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "models/nids_model.pkl")
joblib.dump(encoders, "models/feature_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

print("\nModel saved as models/nids_model.pkl")
print("Feature encoders saved as models/feature_encoders.pkl")
print("Target encoder saved as models/target_encoder.pkl")
print("Done!")
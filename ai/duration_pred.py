import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib


BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "..", "tasks_log.csv")

dataset = pd.read_csv(CSV_PATH)
len_data = len(dataset)

X = dataset[['category', 'importance', 'est_duration', 'energy_at_creation']].values
y = dataset['actual_duration'].values 

# Train-test split
X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Impute missing numeric values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X_train_raw[:, 1:] = imputer.fit_transform(X_train_raw[:, 1:])
X_test_raw[:, 1:] = imputer.transform(X_test_raw[:, 1:])

# One-hot encode category column
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(handle_unknown='ignore'), [0])], remainder='passthrough')
X_train = np.array(ct.fit_transform(X_train_raw))
X_test = np.array(ct.transform(X_test_raw))

if len_data < 50:
    print("Not enough data to train")
    exit()
    
# Train the Random Forest 
regressor = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_leaf=3,
    max_features='sqrt',
    random_state=0,
    n_jobs=-1
)
regressor.fit(X_train, y_train)

# Train XGboost
model = XGBRegressor(
    objective='reg:squarederror',
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate
y_pred = regressor.predict(X_test)
y_pred_boost = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

mae_boost = mean_absolute_error(y_test, y_pred_boost)
rmse_boost = np.sqrt(mean_squared_error(y_test, y_pred_boost))

print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}")
print(f"MAE XGBoost: {mae_boost:.2f}, RMSE XGBoost: {rmse_boost:.2f}")

# Save best model
if mae_boost < mae:
    best_model = model
    best_mae = mae_boost
    print("Using XGBoost model")
else:
    best_model = regressor
    best_mae = mae
    print("Using RandomForest model")

joblib.dump({
    "model": best_model,
    "imputer": imputer,
    "encoder": ct,
    "mae": best_mae 
}, "duration_bundle.pkl")

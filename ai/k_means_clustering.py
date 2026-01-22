import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
import os

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "..", "tasks_log.csv")

dataset = pd.read_csv(CSV_PATH)

# Compute time_of_day and day_of_week from started_time
dataset['started_time'] = pd.to_datetime(dataset['started_time'])
dataset['time_of_day'] = dataset['started_time'].dt.hour
dataset['day_of_week'] = dataset['started_time'].dt.dayofweek  # 0=Monday

# Drop raw datetime columns 
dataset = dataset.drop(columns=['created_time', 'started_time', 'completed_time'])

# Convert to numeric times (already numeric, but safe)
dataset['time_of_day'] = pd.to_numeric(dataset['time_of_day'], errors='coerce')
dataset['day_of_week'] = pd.to_numeric(dataset['day_of_week'], errors='coerce')

# Impute missing numeric values
numeric_cols = ['est_duration', 'actual_duration', 'importance', 'energy_at_creation', 'delay_before_start', 'time_of_day', 'day_of_week']
imputer = SimpleImputer(strategy='mean')
dataset[numeric_cols] = imputer.fit_transform(dataset[numeric_cols])

# Cyclical encoding for time features
dataset['time_of_day_sin'] = np.sin(2 * np.pi * dataset['time_of_day'] / 24)
dataset['time_of_day_cos'] = np.cos(2 * np.pi * dataset['time_of_day'] / 24)
dataset['day_of_week_sin'] = np.sin(2 * np.pi * dataset['day_of_week'] / 7)
dataset['day_of_week_cos'] = np.cos(2 * np.pi * dataset['day_of_week'] / 7)
dataset = dataset.drop(columns=['time_of_day', 'day_of_week'])

X = dataset[['category', 'est_duration', 'actual_duration', 'importance', 'energy_at_creation', 'delay_before_start',
             'time_of_day_sin', 'time_of_day_cos', 'day_of_week_sin', 'day_of_week_cos']].values

# One-hot encoding of catoegry
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = ct.fit_transform(X)

#Feature scaling
sc = StandardScaler()
X = sc.fit_transform(X)

#Elbow method to determine the optimal number of clusters for the model
wcss = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
k_range = range(1, 15)
knee = KneeLocator(k_range, wcss, curve="convex", direction="decreasing")
optimal_clusters = knee.knee

# Fit final K-Means
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', random_state=42, n_init = 10)
y_kmeans = kmeans.fit_predict(X)

print("Cluster assignments:", y_kmeans)

# Interpreting the clusters
dataset['cluster'] = y_kmeans

cluster_summary = dataset.groupby('cluster').agg({'actual_duration': ['mean', 'median', 'std'],'est_duration': ['mean', 'median'],'importance': ['mean', 'median'],'energy_at_creation': ['mean'],'delay_before_start': ['mean'], 'time_of_day' : ['mean', 'median'],'day_of_week': lambda x: x.mode()[0], 'category': lambda x: x.mode()[0]}).reset_index()

def cluster_label(summary):
    # Duration 
    duration = summary[('actual_duration', 'mean')]
    if duration < 20:
        label = "short"
    elif duration > 60:
        label = "long"
    else:
        label = "medium"
    # Time of day 
    tod = summary[('time_of_day', 'mean')]
    if tod < 6:
        label += " night"
    elif tod < 12:
        label += " morning"
    elif tod < 18:
        label += " afternoon"
    else:
        label += " evening"
    
    # Category part
    if ('category', '') in summary.columns:
        cat_label = summary[('category', '')]
    else:
        # fallback if category is not multi-index
        cat_label = summary[('category')]
    
    if not pd.isna(cat_label):
        label += f" ({cat_label})"
    
    return label
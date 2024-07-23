import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load data
data = pd.read_csv('synthetic_truck_maintenance_data.csv')

# Create interaction features
data['location_operation_time'] = data['location'] + '_' + data['operation_time'].astype(str)
data['location_company'] = data['location'] + '_' + data['company']
data['location_engine'] = data['location'] + '_' + data['engine']
data['location_milage'] = data['location'] + '_' + data['milage'].astype(str)
data['company_engine'] = data['company'] + '_' + data['engine']
data['company_milage'] = data['company'] + '_' + data['milage'].astype(str)
data['engine_milage'] = data['engine'] + '_' + data['milage'].astype(str)

# Split data into features and target
X = data.drop('maintenance_needed', axis=1)
y = data['maintenance_needed']

# Define categorical and numerical features
categorical_features = ['location', 'company', 'engine', 'milage', 'location_operation_time', 
                        'location_company', 'location_engine', 'location_milage', 
                        'company_engine', 'company_milage', 'engine_milage']
numerical_features = ['operation_time']

# Preprocessing pipelines for both numerical and categorical data
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

numerical_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Define the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(class_weight='balanced', random_state=42))
])

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter tuning using Grid Search
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [None, 10, 20],
    'classifier__min_samples_split': [2, 5],
    'classifier__min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

# Predict on test set
y_pred = best_model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'Best Parameters: {grid_search.best_params_}')
print(f'Accuracy: {accuracy:.2f}')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
print(f'F1 Score: {f1:.2f}')

# Feature importance
# Get feature names after preprocessing
preprocessor = best_model.named_steps['preprocessor']
onehot_features = list(preprocessor.transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_features))
feature_names = numerical_features + onehot_features
feature_importances = best_model.named_steps['classifier'].feature_importances_

# Create a DataFrame for feature importances
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importances
})

print(feature_importance_df.sort_values(by='importance', ascending=False))

# Save the model
joblib.dump(best_model, 'maintenance_model.pkl')

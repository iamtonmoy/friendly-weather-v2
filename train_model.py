import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset
df = pd.read_csv('dataV1.csv')  # Replace 'your_dataset.csv' with your actual dataset path

# Specify the features and target variable
features = ['Temp', 'Humidity', 'WindSpeed', 'Pressure', 'Visibility']
target = 'Weather'

# Create a DataFrame with only the selected features and the target variable
df = df[features + [target]]

# Convert categorical 'Weather' values to numerical labels if needed
# (assuming RandomForestClassifier can handle categorical labels)
df['Weather'] = pd.Categorical(df['Weather']).codes

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier
model = RandomForestClassifier()

# Train the model
model.fit(X_train, y_train)

# Evaluate the model on the test set if needed
accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy}')

# Save the trained model
joblib.dump(model, 'weather_prediction_model.pkl')
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'


# load csv
df = pd.read_csv('dataV1.csv')  

features = ['Temp', 'Humidity', 'WindSpeed', 'Pressure', 'Visibility']
target = 'Weather'

df = df[features + [target]]


df['Weather'] = pd.Categorical(df['Weather']).codes


X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)


model = RandomForestClassifier()


model.fit(X_train, y_train)


accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy}')

# save the trained model
joblib.dump(model, 'weather_prediction_model.pkl')
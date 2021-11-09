from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
import joblib

from connect_database import get_flight_dataframe

df = get_flight_dataframe()

df.drop('S_no', axis=1, inplace=True)
X = df.drop('Price', axis=1)
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = ExtraTreesRegressor(max_depth=80, min_samples_split=8, n_estimators=20,
                    random_state=14)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
joblib.dump(model, 'best.pkl', compress=3)

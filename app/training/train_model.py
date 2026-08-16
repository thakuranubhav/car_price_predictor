import joblib  
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from train_utils import DATA_FILE_PATH, MODEL_DIR, MODEL_PATH

df = (
    pd
    .read_csv(DATA_FILE_PATH)
    .drop_duplicates()
    .drop(columns=['name', 'model', 'edition'])
)

x=df.drop(columns='selling_price')
y=df.selling_price.copy()

x_train, x_test, y_train, y_test= train_test_split(x,y, test_size=0.2, random_state=43)


num_cols=x_train.select_dtypes(include='number').columns.tolist()
cat_cols=[col for col in x_train.columns  if col not in num_cols]

num_pipeline =Pipeline(steps= [
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(
        handle_unknown='ignore', sparse_output=False
    ))
])

preprocessor= ColumnTransformer(
    transformers=[
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ]
)

regressor=  RandomForestRegressor(
    n_estimators=10, max_depth=5, random_state=42
)

rf_model = Pipeline(steps=[
    ('pre', preprocessor),
    ('reg', regressor)
])

rf_model.fit(x_train, y_train)

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(rf_model, MODEL_PATH)
import pytz
import numpy as np
import pandas as pd
from datetime import datetime
from joblib import dump

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import XCom
from airflow.operators.python import PythonOperator

from sklearn.metrics import mean_absolute_error
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.compose import TransformedTargetRegressor


path_to_data = '/app/clean_data/my_dataset.csv'
file_path_for_model = '/app/models/new_trained_model_regressor.joblib'

my_dag = DAG(
    dag_id='predict_co2_car',
    description='Predict co2 emissions ',
    tags=['project', 'exam', 'co2'],
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(2),
    },
    catchup=False
)


def get_dataset_from_file(path_to_data):
    """ Get data from original file """

    df = pd.read_csv(path_to_data)

    return df


def clean_dataset(df):
    """ Get only good columns for model and clean/replace data from NaN values """

    default_column = ['marque', 'modele', 'carburant', 'hybride', 'puiss_admin', 'puiss_max', 'boite_v', 'co2']

    # get column
    df = df[default_column]

    # replace NaN value and fill null
    df['hybride'] = df['hybride'].astype(str).replace(['nan'], ['non']).fillna('non')
    df = df.dropna(subset=['co2'])

    # reset index
    df = df.reset_index().drop('index', axis=1)

    return df


def encode_variables(df):
    """ Encode categorial variables variables """

    # select numeric variables
    var_num = df[['puiss_admin', 'puiss_max', 'co2']]

    # select  categorial variables
    var_cat = df[['marque', 'modele', 'carburant', 'hybride', 'boite_v']]

    le = preprocessing.LabelEncoder()

    df_cat_encoded = pd.DataFrame()

    for column in var_cat.columns:
        column_encoded = le.fit_transform(var_cat[column])
        column_encoded = pd.DataFrame({column: column_encoded})
        df_cat_encoded = pd.concat([df_cat_encoded, column_encoded], axis=1)

    df = pd.DataFrame(pd.concat([df_cat_encoded, var_num], axis=1))

    return df


def get_clean_dataset():
    """ Pipeline to get clean data """

    df = get_dataset_from_file(path_to_data)
    df = clean_dataset(df)
    df = encode_variables(df)

    return df


def split_dataset():
    """ Split data set with data and target values """

    df = get_clean_dataset()
    data = df.drop(['co2'], axis=1)
    target = df['co2']

    return data, target


def preprocess_train_test_set():
    """ Split trainin and testing test, normalize and apply Smotting"""

    data, target = split_dataset()

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)

    scaler = preprocessing.RobustScaler().fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    return X_train, X_test, y_train, y_test


def pull_last_model_xcom_value(key='mean_absolute_error', index=-1):

    execution_date = datetime.now(pytz.utc)
    xcom_entries = XCom.get_many(
        execution_date=execution_date, task_ids=None, include_prior_dates=True
    )
    xcom_values = [xcom.value for xcom in xcom_entries if xcom.key == key]

    if xcom_values:
        return xcom_values[index]
    else:
        return None


def perform_grid_search(data, target):
    """ Fir model with grid search """

    params_sgdr = {
        'regressor__penalty': ['l1', 'l2'],
        'regressor__alpha': np.linspace(0, 0.0002, 3),
        'regressor__epsilon': np.linspace(0, 0.2, 3)
    }
    grid_sgdr = GridSearchCV(
        TransformedTargetRegressor(regressor=SGDRegressor()),
        param_grid=params_sgdr,
        cv=2,
        scoring=("r2", "neg_mean_absolute_error"),
        refit='neg_mean_absolute_error',
        return_train_score=True,
        verbose=0,
        n_jobs=-1
    )

    grid_sgdr.fit(data, target)

    return grid_sgdr


def predict_score(task_instance):
    ''' Calculates score for prediction'''

    X_train, X_test, y_train, y_test = preprocess_train_test_set()

    grid_sgdr = perform_grid_search(X_train, y_train)

    y_pred = grid_sgdr.predict(X_test)

    mae = np.round(np.round(mean_absolute_error(y_test, y_pred)), 2)

    task_instance.xcom_push(key='mean_absolute_error', value=mae)


def train_and_dump_model(task_instance, file_path_for_model):
    """ If necessary, retrain model """

    data, target = split_dataset()

    last_model_mae = pull_last_model_xcom_value(key='mean_absolute_error', index=1)
    predicted_mae = pull_last_model_xcom_value(key='mean_absolute_error', index=0)

    if predicted_mae < last_model_mae:

        print(predicted_mae)
        print(last_model_mae)

        data = preprocessing.RobustScaler().fit_transform(data)

        trained_model = perform_grid_search(data, target)

        dump(trained_model, file_path_for_model)

    else:
        pass


my_task_1 = PythonOperator(
    task_id='get_predictions',
    python_callable=predict_score,
    retries=5,
    dag=my_dag,
    email_on_retry=True,
    email=['john.doe@datascientest.com']

)

my_task_2 = PythonOperator(
    task_id='pull_last_xcom_value',
    python_callable=train_and_dump_model,
    dag=my_dag
)

my_task_1 >> my_task_2

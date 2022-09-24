# Importing needed library
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from random import uniform
from datetime import datetime

# Setting default argument for start date
default_args = {
    'start_date': datetime(2022, 9, 23),
    'catchup' : False
    }

# Defining training model operator
def _training_model(ti):
    accuracy = uniform(0.1, 10.0)
    print(f'model\'s accuracy: {accuracy}')
    ti.xcom_push(key='model_accuracy', value=accuracy)

# Defining choose best model operator and make xcom pull command
def _choose_best_model(ti):
    print('choose best model')

with DAG('xcom_dag',schedule_interval= '@once', default_args=default_args, catchup=False) as dag:
    downloading_data = BashOperator(
        task_id='downloading_data',
        bash_command='sleep 1',
        do_xcom_push = False
        )
    training_model_task = [
        PythonOperator(
            task_id=f'training_model_{task}',
            python_callable=_training_model
            ) for task in ['A', 'B', 'C']]
    choose_model = PythonOperator(
        task_id='choose_model',
        python_callable=_choose_best_model
        )

# Setting operators dependencies
downloading_data >> training_model_task >> choose_model
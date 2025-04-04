from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
import requests
import os

# Define API and database connection settings
API_URL = "http://api:8001"  # This should match the service name in docker-compose.yml
CHROMADB_URL = "http://chromadb:8000"

# Define DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'chatbot_ai_workflow',
    default_args=default_args,
    schedule_interval="@daily",  # Runs daily
    catchup=False,
    description='An Airflow DAG for Chatbot AI with ChromaDB and Ollama'
)

# Task 1: Extract legal texts
def extract_legal_texts():
    text = "Constitution of 1958 extracted text..."  # Placeholder: Load actual text
    with open('/opt/airflow/data/constitution.txt', 'w') as f:
        f.write(text)

extract_task = PythonOperator(
    task_id='extract_legal_texts',
    python_callable=extract_legal_texts,
    dag=dag
)

# Task 2: Vectorize and Store in ChromaDB
def vectorize_texts():
    text = open('/opt/airflow/data/constitution.txt', 'r').read()
    response = requests.post(f"{CHROMADB_URL}/store", json={"text": text})
    if response.status_code == 200:
        print("Text stored in ChromaDB.")

vectorize_task = PythonOperator(
    task_id='vectorize_texts',
    python_callable=vectorize_texts,
    dag=dag
)

# Task 3: Query Chatbot API
query_task = SimpleHttpOperator(
    task_id='query_chatbot',
    http_conn_id='chatbot_api',  # Needs to be set in Airflow Connections UI
    endpoint='/query',
    method='POST',
    data={"question": "What are the main laws of the Constitution?"},
    headers={"Content-Type": "application/json"},
    response_filter=lambda response: response.text,
    log_response=True,
    dag=dag
)

# Task 4: Log Queries to Database
def log_queries():
    response = requests.post(f"{API_URL}/log_query", json={"query": "What are the main laws?"})
    print(response.json())

log_queries_task = PythonOperator(
    task_id='log_queries',
    python_callable=log_queries,
    dag=dag
)

# Task 5: Run Benchmarking Script
def run_benchmark():
    os.system("python /opt/airflow/scripts/benchmark.py")

benchmark_task = PythonOperator(
    task_id='run_benchmark',
    python_callable=run_benchmark,
    dag=dag
)

# Task Dependencies
extract_task >> vectorize_task >> query_task >> log_queries_task >> benchmark_task

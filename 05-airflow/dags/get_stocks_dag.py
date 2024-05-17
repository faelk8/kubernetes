from pathlib import Path
import pendulum
import yfinance
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.macros import ds_add
from kubernetes.client import models as k8s

TICKERS = [
    "AAPL",
    "MSFT",
    "GOOG",
    "TSLA"
]

executor_config = {
    # crias uma pasta data dentro do Pod de execução da tarefa do DAG;
    # cria um volume stock-volume dentro do Pod;
    # conectas a pasta data ao volume stock-volume;
    # conecta stock-volume ao objeto de reinvidicação de volume airflow-data-claim, que havíamos criado anteriormente.
    "pod_override": k8s.V1Pod(spec=k8s.V1PodSpec(
        
        containers=[
            k8s.V1Container(
                name="base",
                volume_mounts=[
                    k8s.V1VolumeMount(mount_path="/data/", name="stock-volume")
                ],
            )
        ],
        volumes=[
            k8s.V1Volume(
                name="stock-volume",
                persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
                    claim_name="airflow-data-claim"
                )
            )
        ]))
}

@task(executor_config=executor_config)
def get_history(ticker, ds=None, ds_nodash=None):
    file_path = f"/data/{ticker}/{ticker}_{ds_nodash}.csv"
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    yfinance.Ticker(ticker).history(
        period="1d", 
        interval="1h",
        start=ds_add(ds, -1),
        end=ds,
        prepost=True,
    ).to_csv(file_path)

@dag(
    schedule_interval="0 0 * * *",
    start_date=days_ago(1),
    catchup=True
)
def get_crypto_dag():
    for ticker in TICKERS:
        get_history.override(task_id=ticker)(ticker)
    

dag = get_crypto_dag()
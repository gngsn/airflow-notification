import pendulum
from airflow.decorators import dag, task


@task.virtualenv(
    task_id="virtualenv_python", requirements=["colorama==0.4.0"], system_site_packages=False
)
def callable_virtualenv():
    from time import sleep

    from colorama import Back, Fore, Style

    print(Fore.RED + "some red text")
    print(Back.GREEN + "and with a green background")
    print(Style.DIM + "and in dim text")
    print(Style.RESET_ALL)
    for _ in range(4):
        print(Style.DIM + "Please wait...", flush=True)
        sleep(1)
    print("Finished")


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example"],
)
def test_print_color_log_dag():
    callable_virtualenv()


trigger_dag = test_print_color_log_dag()

print("done!")

if __name__ == "__main__":
    trigger_dag.test()

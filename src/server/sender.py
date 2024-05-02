import procrastinate

app = procrastinate.App(connector=procrastinate.SyncPsycopgConnector())


@app.task(queue="sums")
def sum(a, b):
    with open("myfile", "w") as f:
        f.write(str(a + b))


with app.open():
    sum.defer(a=3, b=5)

app.run_worker(queues=["sums"])

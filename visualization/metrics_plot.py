import matplotlib.pyplot as plt

def plot_metrics(metrics):
    data = metrics.summary()

    names = list(data.keys())
    values = list(data.values())

    plt.figure()
    plt.bar(names, values)
    plt.title("Simulation Metrics")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("results/graphs/metrics.png")
    plt.show()
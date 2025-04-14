import os
import matplotlib.pyplot as plt
import numpy as np
from TandemSystem import TandemSystem


def statistics(tandem: TandemSystem):
    
    os.makedirs('./figures', exist_ok=True)

    timeline_data = []

    for consumer_id in range(tandem.served_consumers):
        if consumer_id not in tandem.first_queue_arrivals:
            continue
        t_first_queue = tandem.first_queue_arrivals.get(consumer_id, None)
        t_first_server = tandem.first_server_arrivals.get(consumer_id, None)
        t_second_queue = tandem.second_queue_arrivals.get(consumer_id, None)
        t_departure = tandem.second_server_departures.get(consumer_id, None)

        if None in [t_first_queue, t_first_server, t_second_queue, t_departure]:
            continue

        timeline_data.append((consumer_id, t_first_queue, t_first_server, t_second_queue, t_departure))

    total_system_times = [t3 - t0 for (_, t0, _, _, t3) in timeline_data]
    first_server_times = [t2 - t1 for (_, _, t1, t2, _) in timeline_data]
    second_server_times = [t3 - t2 for (_, _, _, t2, t3) in timeline_data]
    first_server_awaits = [t1 - t0 for (_, t0, t1, _, _) in timeline_data]
    second_server_awaits = [0 if t2 == t1 else t2 - t1 for (_, _, t1, t2, _) in timeline_data]

    return {
        'total_system_times': total_system_times,
        'first_server_times': first_server_times,
        'second_server_times': second_server_times,
        'first_server_awaits': first_server_awaits,
        'second_server_awaits': second_server_awaits,
        'total_consumidores': len(timeline_data)
    }

def graphic_total_times(stats: dict):
    times = stats['total_system_times']
    mean = np.mean(times)
    median = np.median(times)

    os.makedirs('./figures', exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Media = {mean:.2f} min')
    plt.axvline(median, color='green', linestyle='--', linewidth=2, label=f'Mediana = {median:.2f} min')

    plt.title("Distribución de tiempos en el sistema")
    plt.xlabel("Tiempo en el sistema (minutos)")
    plt.ylabel("Cantidad de consumidores")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('./figures/tiempos_en_sistema.png')
    plt.close()

def bootstrap_total_time_mean(stats: dict, iterations=1000, trust_level=0.95):
    total_times = np.array(stats['total_system_times'])
    n = len(total_times)

    bootstrapped_means = []
    for _ in range(iterations):
        muestra = np.random.choice(total_times, size=n, replace=True)
        bootstrapped_means.append(np.mean(muestra))
    bootstrapped_means = np.array(bootstrapped_means)

    alpha = 1 - trust_level
    lower = np.percentile(bootstrapped_means, 100 * alpha / 2)
    upper = np.percentile(bootstrapped_means, 100 * (1 - alpha / 2))
    original_mean = np.mean(total_times)

    os.makedirs('./figures', exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.hist(bootstrapped_means, bins=30, color='lightgreen', edgecolor='black', alpha=0.8)
    plt.axvline(original_mean, color='red', linestyle='--', label=f'Media original = {original_mean:.2f}')
    plt.axvline(lower, color='blue', linestyle='--',
                label=f'IC {int(trust_level * 100)}%: [{lower:.2f}, {upper:.2f}]')
    plt.axvline(upper, color='blue', linestyle='--')
    plt.title("Distribución bootstrap de la media del tiempo en el sistema")
    plt.xlabel("Media del tiempo en el sistema (min)")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('./figures/bootstrap_media_tiempo.png')
    plt.close()

def bootstrap_total_time_median(stats: dict, iterations=1000, trust_level=0.95):
    total_times = np.array(stats['total_system_times'])
    n = len(total_times)

    bootstrapped_medians = []
    for _ in range(iterations):
        muestra = np.random.choice(total_times, size=n, replace=True)
        bootstrapped_medians.append(np.median(muestra))
    bootstrapped_medians = np.array(bootstrapped_medians)

    alpha = 1 - trust_level
    lower = np.percentile(bootstrapped_medians, 100 * alpha / 2)
    upper = np.percentile(bootstrapped_medians, 100 * (1 - alpha / 2))
    original_median = np.median(total_times)

    os.makedirs('./figures', exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.hist(bootstrapped_medians, bins=30, color='lightgreen', edgecolor='black', alpha=0.8)
    plt.axvline(original_median, color='red', linestyle='--', label=f'Mediana original = {original_median:.2f}')
    plt.axvline(lower, color='blue', linestyle='--',
                label=f'IC {int(trust_level * 100)}%: [{lower:.2f}, {upper:.2f}]')
    plt.axvline(upper, color='blue', linestyle='--')
    plt.title("Distribución bootstrap de la mediana del tiempo en el sistema")
    plt.xlabel("Mediana del tiempo en el sistema (min)")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('./figures/bootstrap_mediana_tiempo.png')
    plt.close()
import numpy as np

from hyper_log_log.hyper_log_log import HyperLogLog


def theoretical_error_rate(nb_bucket):
    return 1.04 / np.sqrt(nb_bucket)


def experimental_error_rate(nb_buckets, cardinality, nb_iterations=1):
    error_rate_list = []
    for _ in range(nb_iterations):
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        for item in range(cardinality):
            hyper_log_log.add_item(item=item)
        _cardinality = hyper_log_log.estimate_cardinality()
        error_rate_list.append(abs(cardinality - _cardinality) / cardinality)
    return np.median(error_rate_list)

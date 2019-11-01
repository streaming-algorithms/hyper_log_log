import logging

from hyper_log_log.tools import experimental_error_rate, theoretical_error_rate


def hyper_log_log_benchmark(nb_buckets, cardinality, nb_iterations=1):
    logger = logging.getLogger(__name__)
    exp_error_rate = experimental_error_rate(
        nb_buckets=nb_buckets,
        cardinality=cardinality,
        nb_iterations=nb_iterations
    )
    the_error_rate = theoretical_error_rate(nb_bucket=nb_buckets)
    logger.info(f'Experimental error rate: {exp_error_rate}'
                f'Theoretical error rate: {the_error_rate}')
    return exp_error_rate, the_error_rate

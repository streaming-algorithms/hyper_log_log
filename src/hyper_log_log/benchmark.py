import logging

from streaming_algorithms.bloom_filter.bloom_filter import BloomFilter
from streaming_algorithms.bloom_filter.tools import false_positive_rate


def bloom_filter_benchmark(bit_array_size, nb_salt, input_cardinal):
    logger = logging.getLogger(__name__)
    bloom_filter = BloomFilter(bit_array_size=bit_array_size, nb_salt=nb_salt)

    for item in range(input_cardinal):
        bloom_filter.add_item(item=item)
    false_negative_count = 0

    for item in range(input_cardinal):
        if not bloom_filter.retrieve_item(item=item):
            false_negative_count += 1
    exp_false_negative_rate = false_negative_count / input_cardinal
    the_false_negative_rate = 0
    logger.info(f'False negative rate: {exp_false_negative_rate} '
                f'should be {the_false_negative_rate}')
    assert exp_false_negative_rate == 0

    false_positive_count = 0
    for item in range(input_cardinal, 101 * input_cardinal):
        if bloom_filter.retrieve_item(item=item):
            false_positive_count += 1
    exp_false_positive_rate = false_positive_count / (100 * input_cardinal)
    the_false_positive_rate = false_positive_rate(bit_array_size=bit_array_size,
                                                  nb_salt=nb_salt,
                                                  input_cardinal=input_cardinal)
    logger.info(f'False positive rate: {exp_false_positive_rate}'
                f'should be >= {the_false_positive_rate} ')
    assert exp_false_positive_rate <= the_false_positive_rate

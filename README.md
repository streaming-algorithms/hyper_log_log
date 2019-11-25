# HyperLogLog

#### Definition:

__HyperLogLog__ is a space efficient probabilistic data structures used to compute a 
count distinct over a stream.

HyperLogLog is constituted by __m__ buckets. The goal is to estimate __n__ the 
stream's cardinality.


__Adding an element to HyperLogLog:__ compute __b__ = binary hash of the input item.
The first bits of __b__ will define the bucket index. This bucket will receive 
max(bucket content, #leading zeros in __b__)

__Estimating cardinality:__ compute n = a  m<sup>2</sup> 2<sup>harmonic mean over 
buckets</sup> where __a__ is a correction constant.


#### Relative error:
The relative error of HyperLogLog is 1.04 / m<sup>1/2</sup>.


#### Usage:
Install the HyperLogLog library. Go to the hyper_log_log folder and run:
```bash
pip install .
```

The class __HyperLogLog__ can be used to create a HyperLogLog instance with a custom 
number of buckets __m__.

```python
from hyper_log_log import HyperLogLog

hyper_log_log = HyperLogLog(nb_buckets=m)
```

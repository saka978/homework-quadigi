from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

class MeasType(Enum):
    SPO2 = 1
    HR = 2
    TEMP = 3

@dataclass
class Measurement:
    measurementTime: datetime
    measurementType: MeasType
    value: float

def print_out_measurements(sampled_measurements):
    for meas_type, samples in sampled_measurements.items():
        print(f"Measurements for {meas_type.name}:")
        for sample in samples:
            print(f"{sample.measurementTime}, {sample.value}")

def sample_measurements(startOfSampling: datetime, unsampledMeasurements: list[Measurement]) -> dict[MeasType, list[Measurement]]:
    sampled_measurements = defaultdict(list)
    grouped_measurements = _group_measurements_by_type(unsampledMeasurements)
    for meas_type, measurements in grouped_measurements.items():
        filtered_measurements = [measurement for measurement in measurements if measurement.measurementTime >= startOfSampling]
        buckets = _bucket_measurement_into_time_interval(filtered_measurements)
        sampled_measurements = _select_last_measurement_from_each_interval(buckets, meas_type, sampled_measurements)
    sampled_measurements = _sort_measurements(sampled_measurements)

    return sampled_measurements

def _group_measurements_by_type(unsampledMeasurements: list[Measurement]):
    grouped_measurements = defaultdict(list)
    for measurement in unsampledMeasurements:
        grouped_measurements[measurement.measurementType].append(measurement)
    return grouped_measurements

def _bucket_measurement_into_time_interval(measurements):
    buckets = defaultdict(list)
    for measurement in measurements:
        interval_start = measurement.measurementTime.replace(second=0, microsecond=0)
        minute = (measurement.measurementTime.minute // 5) * 5
        interval_start = interval_start.replace(minute=minute)
        if measurement.measurementTime > interval_start:
            interval_start += timedelta(minutes=5)
        buckets[interval_start].append(measurement)

    return buckets

def _select_last_measurement_from_each_interval(buckets, meas_type, container):
    for interval_start, bucket in buckets.items():
        last_measurement = max(bucket, key=lambda measurement: measurement.measurementTime)
        last_measurement.measurementTime = interval_start
        container[meas_type].append(last_measurement)

    return container

def _sort_measurements(sampled_measurements):
    for meas_type in sampled_measurements:
        sampled_measurements[meas_type].sort(key=lambda measurement: measurement.measurementTime)

    return sampled_measurements
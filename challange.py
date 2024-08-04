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

def sampleMeasurements(startOfSampling: datetime, unsampledMeasurements: list[Measurement]) -> dict[MeasType, list[Measurement]]:
    # Group measurements by type
    sampled_measurements = defaultdict(list)
    grouped_measurements = groupMeasurementsByType(unsampledMeasurements)
    
    # Process each type of measurement separately
    for meas_type, measurements in grouped_measurements.items():
        # Bucket measurements into 5-minute intervals
        buckets = bucketMeasurementIntoTimeIntervals(measurements)
        
        #sampled_measurements = selectLastMeasurementFromEachInterval(buckets)
        # Select the last measurement from each interval
        
        for interval_start, bucket in buckets.items():
            last_measurement = max(bucket, key=lambda m: m.measurementTime)
            # Align the measurement time to the interval start
            last_measurement.measurementTime = interval_start
            sampled_measurements[meas_type].append(last_measurement)
    
    # Sort the output by time
    for meas_type in sampled_measurements:
        sampled_measurements[meas_type].sort(key=lambda m: m.measurementTime)
    
    return sampled_measurements

def groupMeasurementsByType(unsampledMeasurements: list[Measurement]):
    grouped_measurements = defaultdict(list)
    for measurement in unsampledMeasurements:
        grouped_measurements[measurement.measurementType].append(measurement)
    return grouped_measurements

def bucketMeasurementIntoTimeIntervals(measurements):
    buckets = defaultdict(list)
    for measurement in measurements:
        # Calculate the 5-minute interval this measurement falls into
        interval_start = measurement.measurementTime.replace(second=0, microsecond=0)
        minute = (measurement.measurementTime.minute // 5) * 5
        interval_start = interval_start.replace(minute=minute)
        # Adjust the interval to the next 5-minute mark if it's not exactly on the border
        if measurement.measurementTime > interval_start:
            interval_start += timedelta(minutes=5)
        buckets[interval_start].append(measurement)
    return buckets

def selectLastMeasurementFromEachInterval(buckets):
    sampled_measurements = defaultdict(list)
    # Select the last measurement from each interval
    for interval_start, bucket in buckets.items():
        last_measurement = max(bucket, key=lambda m: m.measurementTime)
        # Align the measurement time to the interval start
        last_measurement.measurementTime = interval_start
        sampled_measurements[meas_type].append(last_measurement)
    return sampled_measurements

# Example usage:
measurements = [
    Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.TEMP, 35.79),
    Measurement(datetime(2017, 1, 3, 10, 1, 18), MeasType.SPO2, 98.78),
    Measurement(datetime(2017, 1, 3, 10, 9, 7), MeasType.TEMP, 35.01),
    Measurement(datetime(2017, 1, 3, 10, 3, 34), MeasType.SPO2, 96.49),
    Measurement(datetime(2017, 1, 3, 10, 2, 1), MeasType.TEMP, 35.82),
    Measurement(datetime(2017, 1, 3, 10, 5, 0), MeasType.SPO2, 97.17),
    Measurement(datetime(2017, 1, 3, 10, 5, 1), MeasType.SPO2, 95.08)
]

sampled = sampleMeasurements(datetime(2017, 1, 3, 10, 0, 0), measurements)

for meas_type, samples in sampled.items():
    print(f"Measurements for {meas_type.name}:")
    for sample in samples:
        print(f"  {sample.measurementTime}, {sample.value}")

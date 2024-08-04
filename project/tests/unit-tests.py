import unittest
from datetime import datetime
from project.main.sampling import MeasType, Measurement, sample_measurements

class TestSampling(unittest.TestCase):
    start_of_sampling = datetime(2017, 1, 3, 10, 0, 0)

    measurements_before_start_date = [
        Measurement(datetime(2017, 1, 3, 9, 4, 45), MeasType.TEMP, 36.79),
        Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.TEMP, 35.99),
        Measurement(datetime(2017, 1, 3, 9, 4, 45), MeasType.HR, 60),
        Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.HR, 80),
        Measurement(datetime(2017, 1, 3, 9, 4, 45), MeasType.SPO2, 45),
        Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.SPO2, 50)
    ]

    measurement_last_value_is_taken = [
        Measurement(datetime(2017, 1, 3, 10, 4, 50), MeasType.TEMP, 0),
        Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.TEMP, 1)
    ]

    measurement_five_minute_border = [
        Measurement(datetime(2017, 1, 3, 10, 5, 00), MeasType.TEMP, 0),
        Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.TEMP, 1),
        Measurement(datetime(2017, 1, 3, 10, 6, 00), MeasType.TEMP, 2),
    ]

    def test_measurements_are_not_included_before_start_date(self):
        sampled_measurements = sample_measurements(self.start_of_sampling, self.measurements_before_start_date)
        for meas_type in MeasType:
            temp_measurements = sampled_measurements[meas_type]
            self.assertTrue(all(m.measurementTime >= self.start_of_sampling for m in temp_measurements))

    def test_last_measurements_is_taken(self):
        expected_output = Measurement(datetime(2017, 1, 3, 10, 4, 50), MeasType.TEMP, 0)

        sampled_measurements = sample_measurements(self.start_of_sampling, self.measurement_last_value_is_taken)
        filtered_value = sampled_measurements[expected_output.measurementType][0].value
        self.assertTrue(len(sampled_measurements[MeasType.TEMP]) == 1)
        self.assertTrue(filtered_value == expected_output.value)

    def test_five_minute_interval_border(self):
        measurement_expected_result = [
            Measurement(datetime(2017, 1, 3, 10, 5, 00), MeasType.TEMP, 0),
            Measurement(datetime(2017, 1, 3, 10, 10, 00), MeasType.TEMP, 2),
        ]
        sampled_measurements = sample_measurements(self.start_of_sampling, self.measurement_five_minute_border)
        self.assertTrue(len(sampled_measurements[MeasType.TEMP]) == 2)
        self.assertTrue(sampled_measurements[MeasType.TEMP] == measurement_expected_result)
        
if __name__ == '__main__':
    unittest.main()
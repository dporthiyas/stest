__author__ = 'timothyahong'
from extractors import extract_cap_values, extract_other_sensors
from post_process import print_results
from stabilizers import LinearStabilizer
from regression_runners import LinearRegressionRunner
from volume_estimators import SimpleVolumeEstimator
from experiment_parsers import load_experiment_folder


def run_pressure_sensor_regression(data_files, data_parameters, stabilizer, volume_estimator, regression_runner):
    regression_results = {}
    stabilized_volume_results = {}
    volume_results = {}
    for (data_file_name, data_file) in data_files.items():
        if len(data_file) > 0:
            cap_values = extract_cap_values(data_parameters, data_file)
            other_sensor_values = extract_other_sensors(data_parameters, data_file)
            regression_xs = stabilizer.generate_inputs(cap_values, other_sensor_values)
            regression_results[data_file_name] = regression_runner.run(cap_values, regression_xs)
            stabilized_volume_results[data_file_name] = volume_estimator.estimate(regression_results[data_file_name]['stabilized_caps'])
            volume_results[data_file_name] = volume_estimator.estimate(cap_values)
    print_results(regression_results, volume_results, stabilized_volume_results)


stabilizer = LinearStabilizer()
regression_runner = LinearRegressionRunner()
volume_estimator = SimpleVolumeEstimator()
data = load_experiment_folder('/Users/timothyahong/Google Drive/Sensassure/Venture Related/Product/V4 Prototype/Volume Detection/V4.5/nov14_danny')

run_pressure_sensor_regression(
    data_files=data['files'],
    data_parameters=data['parameters'],
    stabilizer=stabilizer,
    volume_estimator=volume_estimator,
    regression_runner=regression_runner
)

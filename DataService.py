import DataRepository as dr
import numpy as np



predicted_data=[]
NUM_SIMULATIONS = 100
def forecastData(data):
    for hour in range (0,24):
        real_values_per_hour = data[hour]
        print(f"For {hour} : {real_values_per_hour}")
        std_dev_by_real_value = round(np.std(data[hour], ddof=1))
        print(f"For std_dev_by_real_value for {hour}: {std_dev_by_real_value} ")
        simulated_mean = []
        for point in range (0, len(real_values_per_hour)):
            simulated_values = np.random.normal(real_values_per_hour[point], std_dev_by_real_value, NUM_SIMULATIONS)
            print(f"For simulated values for {hour}: per {point} = {simulated_values}")
            mean = round(np.mean(simulated_values),2)
            simulated_mean.append(mean)
            # print(f"MEAN: {mean}")
        predicted_mean = round(np.mean(simulated_mean),2)
        predicted_data.append(predicted_mean)
        # return mean
        print(f"Predicted data: {predicted_data}, length : {len(predicted_data)} ")
    return predicted_data




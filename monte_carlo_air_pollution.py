import random
import csv


class City:
    def __init__(self, population, industrialization_level):
        self.population = population
        self.industrialization_level = industrialization_level
        self.wind_speed = random.uniform(10, 25)
        self.temperature = random.uniform(-10, 25)
        self.humidity = random.uniform(0, 100)
        self.pollutant_concentration = random.uniform(0, 100)
        self.rain = random.uniform(0.1,1)
        self.number_vehicles_per_capita = random.uniform(0, 5)
        self.pollution_levels = []
        self.heavy_metal_pollution_levels = []
        self.green_house_gas_emissions_levels = []

    def simulate_pollution(self, num_simulations):

        for _ in range(num_simulations):
            pollution_level = self.population * self.industrialization_level * self.wind_speed * self.rain * random.uniform(0.5, 2.0)
            heavy_metal_pollution_levels = self.population * self.industrialization_level * self.wind_speed *  self.number_vehicles_per_capita * self.rain * random.uniform(0.1, 1.0)
            green_house_gas_emissions_levels = self.population * self.industrialization_level * self.wind_speed * self.temperature* self.pollutant_concentration * random.uniform(0.5, 1.0)
            self.pollution_levels.append(pollution_level)
            self.heavy_metal_pollution_levels.append(heavy_metal_pollution_levels)
            self.green_house_gas_emissions_levels.append(green_house_gas_emissions_levels)


def main():
    # Initialize parameters for the city
    population = int(input("Enter population of the city: "))
    industrialization_level = float(input("Enter industrialization level of the city (0 to 1): "))
    num_simulations = int(input("Enter number of simulations to run: "))

    # Create a city object
    city = City(population, industrialization_level)

    # Simulate pollution for the city over the specified duration and number of simulations
    city.simulate_pollution(num_simulations)

    # Save results to CSV file
    with open('pollution_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Simulation', 'Pollution Level'])
        for i, pollution_level in enumerate(city.pollution_levels):
            writer.writerow([i+1, pollution_level])

    print("Results saved to 'pollution_results.csv'")

if __name__ == "__main__":
    main()

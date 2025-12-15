from load_data import load_data

#TODO 1: Summary of program
# * Keep reading commands from the user
# * Parse the command
# * Call the right function
# * Print the result
# * Loop until the user exist (Ctrl + C)

#TODO 2: Commands the program supports
#   Help:
#   *   Print available commands
#   show_countries
#   *   Extract all ship countries
#   *   Remove duplicates
#   *   Sort alphabetically
#   *   Print one per line
#   top_countries <num>
#   *   Count ships per country
#   *   Sort by count (descending)
#   *   Print the top <num> countries with counts

#TODO 3:


ships = load_data()["data"]


def get_all_countries(all_data):
	"""Get valid countries by guarding against empty countries in  ships data """
	return [ship["COUNTRY"] for ship in ships if ship.get("COUNTRY")]


def show_countries(all_data):
	"""Display countries in alphabetical order and remove any duplicates"""
	countries = sorted(set(get_all_countries(all_data)))

	for country in countries:
		print(country)


def top_countries(all_data, num_countries):
	country_counts = {}

	for country in get_all_countries(all_data):
		if country in country_counts:
			country_counts[country] += 1
		else:
			country_counts[country] = 1
		#country_counts[country] = country_counts.get(country, 0) + 1

	sorted_countries = sorted(
		country_counts.items(),
		key=lambda item: item[1],
		reverse=True
	)

	for country, count in sorted_countries[:num_countries]:
		print(f"{country}: {count}")


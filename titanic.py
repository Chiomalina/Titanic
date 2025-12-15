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

# Load the JSON file once, and keep only the "data" list (ships)
ships = load_data()["data"]

COMMANDS = {
	"help": help_cmd,
	"show_countries": show_countries_cmd,
	"top_countries": top_countries_cmd,
}


def get_all_countries(all_data):
	"""
	Steps:
	1) Loop through every ship dictionary.
	2) Pick only ships that actually have a COUNTRY value (not None / empty string).
	3) Return a list of country strings.
	"""
	# NOTE: Use 'all_data' (the function parameter), not the global 'ships'
	return [ship["COUNTRY"] for ship in all_data if ship.get("COUNTRY")]


def show_countries(all_data, args):
	"""
	Steps:
	1) Get all country values (may include duplicates).
	2) Convert to a set to remove duplicates.
	3) Sort alphabetically.
	4) Print one country per line.
	"""
	countries = []

	for ship in all_data:
		if ship.get("COUNTRY"):
			countries.append(ship["COUNTRY"])

	unique_countries = set(countries)
	sorted_countries = sorted(unique_countries)

	for country in sorted_countries:
		print(country)



def top_countries_cmd(all_data, args):
	"""
	Steps:
	1) Get all valid country values.
	2) Count how many ships belong to each country (dictionary counting).
	3) Sort the (country, count) pairs by count descending.
	4) Print only the top N results.
	"""
	if len(args) != 1:
		print("Usage: top_countries <num_countries>")
		return

	try:
		num_countries = int(args[0])
	except ValueError:
		print("num_countries must be an integer (e.g., top_countries 5)")
		return

	country_counts = {}
	for ship in all_data:
		country = ship.get("COUNTRY")
		if not country:
			continue
		country_counts[country] = country_counts.get(country, 0) + 1

	sorted_countries = sorted(country_counts.items(), key=lambda item: item[1], reverse=True)

	for country, count in sorted_countries[:num_countries]:
		print(f"{country}: {count}")


def unknown_cmd(all_data, ards):
	print("Unknown command. Type 'help' to seee available commands.")


def help_command(all_data, args):
	"""
	Steps:
	1) Print all commands CLI supports.
	"""
	print("Available commands:")
	print(" help")
	print(" show_countries")
	print(" top_countries <num_countries>")
	print(" exit")


def run_cli(all_data):
	"""
	Steps:
	1) Print a welcome message.
	2) Enter an infinite loop (CLI runs until Ctrl+C).
	3) Read user input, clean it, split into parts.
	4) Use the first part as the command.
	5) Validate arguments (like top_countries needs a number).
	6) Call the matching function.
	7) Handle Ctrl+C cleanly to exit.
	"""
	print("Welcome to the Ships CLI. Type 'help' for commands. Ctrl+C or 'exir' to quit.")

	while True:
		try:
			user_input = input("> ").strip()
			parts = user_input.split()

			# If user just pressed Enter, do nothing and ask again
			if not parts:
				continue

			command = parts[0]

			if command == "help":
				print_help()

			elif command == "show_countries":
				show_countries(all_data)

			elif command == "top_countries":
				# Expect exactly: ["top_countries", "5"]
				if len(parts) != 2 or not parts[1].isdigit():
					print("Usage: top_countries <num_countries>")
					continue

				num_countries = int(parts[1])
				top_countries(all_data, num_countries)

			else:
				print("Unknown command. Type 'help'.")

		except KeyboardInterrupt:
			print("\nExiting CLI.")
			break

		handler = COMMANDS.get(command, unknown_cmd)
		handler(all_data, args)


if __name__ == "__main__":
	run_cli(ships)

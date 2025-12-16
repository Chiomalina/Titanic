from load_data import load_data
import sys

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

# ----------------------------
# Data loading (run once)
# ----------------------------
# Load the JSON file once, and keep only the "data" list (ships)
ships = load_data()["data"]


# ----------------------------
# Command functions
# ----------------------------
def get_all_countries(all_data):
	"""
	Returns a list of COUNTRY values from the ships data.

	Steps:
	1) Loop through every ship dictionary.
	2) Guard against missing/empty COUNTRY values using ship.get("COUNTRY").
	3) Collect and return the valid country strings.
	"""
	# NOTE: Use 'all_data' (the function parameter), not the global 'ships'
	return [ship["COUNTRY"] for ship in all_data if ship.get("COUNTRY")]


def help_cmd(all_data, args):
	"""
	Print a list of commands supported by this CLI.

	Reads directly from the COMMANDS dictionary,
	so adding a new command automatically updates the help output.
	"""
	print("Available commands:")

	for command in sorted(COMMANDS.keys()):
		print(f"  {command}")

	print("  exit")


def show_countries_cmd(all_data, args):
	"""
	Print all ship countries (no duplicates) in alphabetical order.

	Steps:
	1) Get all valid country values.
	2) Convert to a set to remove duplicates.
	3) Sort alphabetically.
	4) Print one country per line.
	"""
	countries = get_all_countries(all_data)
	unique_countries = set(countries)
	sorted_countries = sorted(unique_countries)

	for country in sorted_countries:
		print(country)



def top_countries_cmd(all_data, args):
	"""
	Print the top N countries with the most ships

	Steps:
	1) Validate that we got exactly 1 argument.
	2) Convert it into int.
	3) Count ships per country using a dictionary.
	4) Sort the (country, count) pairs by count descending.
	5) Print only the top N results.
	"""
	# 1) Validate args
	if len(args) != 1:
		print("Usage: top_countries <num_countries>")
		return

	# 2) Parse int safely
	try:
		num_countries = int(args[0])
	except ValueError:
		print("num_countries must be an integer (e.g., top_countries 5)")
		return

	if num_countries <= 0:
		print("num_countries must be a positive integer (e.g., top_countries 5)")
		return

	# 3) Count countries
	country_counts = {}
	for country in get_all_countries(all_data):
		country_counts[country] = country_counts.get(country, 0) + 1

	# 4) Sort by count desc
	sorted_countries = sorted(country_counts.items(), key=lambda item: item[1], reverse=True)

	# 5) Print top N
	for country, count in sorted_countries[:num_countries]:
		print(f"{country}: {count}")


def unknown_cmd(all_data, ards):
	"""
	Fallback handler when the user types an unknown command.
	"""
	print("Unknown command. Type 'help' to see available commands.")


# ----------------------------
# Dispatcher dictionary (function pointers)
# ----------------------------
COMMANDS = {
	"help": help_cmd,
	"show_countries": show_countries_cmd,
	"top_countries": top_countries_cmd,
	# NOTE: "exit" is handled in run_cli because it breaks the loop.
}


# ----------------------------
# Main CLI loop
# ----------------------------
def run_cli(all_data):
	"""
	Run the command line interface (CLI)

	Steps:
	1) Print a welcome message.
	2) Loop forever reading user input.
	3) Split input into:
	   - command (first word)
	   - args (the rest of the words)
	4) If command is "exit" -> break.
	5) Otherwise, look up the function in COMMANDS and call it.
	6) Ctrl+C exits cleanly.
	"""
	print("Welcome to the Ships CLI.")
	print("Type 'help' for commands. 'exit' to quit.")

	try:
		while True:
			user_input = input("> ").strip()

			# If user just pressed Enter, ask again
			if not user_input:
				continue

			# Split input into command and args
			parts = user_input.split()
			command = parts[0]
			args = parts[1:]

			# Handle existing the loop (not part of dispatch)
			if command == "exit":
				print("Existing CLI")
				break

			# Dispatcher lookup: get the handler function
			handler = COMMANDS.get(command, unknown_cmd)

			# Call the handler with (all_date, args)
			handler(all_data, args)

	except KeyboardInterrupt:
		print("\nExiting CLI.")
		sys.exit(0)



if __name__ == "__main__":
	run_cli(ships)

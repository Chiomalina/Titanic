from load_data import load_data
from collections import Counter
import matplotlib.pyplot as plt
import sys


# ----------------------------
# Helpers
# ----------------------------
def get_all_countries(all_data):
    """Return a list of valid ship COUNTRY values (skips missing/empty)."""
    return [ship["COUNTRY"] for ship in all_data if ship.get("COUNTRY")]


def get_lat_lon(ship):
    """Return (lat, lon) as floats or (None, None) if invalid/missing."""
    try:
        lat = float(ship.get("LAT"))
        lon = float(ship.get("LON"))
    except (TypeError, ValueError):
        return None, None

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None, None

    return lat, lon


def parse_positive_int(value, usage_message):
    """Convert value to a positive int or print usage and return None."""
    try:
        number = int(value)
    except ValueError:
        print(usage_message)
        return None

    if number <= 0:
        print(usage_message)
        return None

    return number


# ----------------------------
# Command functions
# ----------------------------
def help_cmd(all_data, args):
    """Print all available commands."""
    print("Available commands:\n")

    for command in sorted(COMMANDS_HELP.keys()):
        print(f"  {command}")
        print(f"      {COMMANDS_HELP[command]}\n")


def show_countries_cmd(all_data, args):
    """Print all ship countries (unique, alphabetical)."""
    countries = sorted(set(get_all_countries(all_data)))
    for country in countries:
        print(country)


def top_countries_cmd(all_data, args):
    """Print the top N countries by ship count."""
    if len(args) != 1:
        print("Usage: top_countries <num_countries>")
        return

    num_countries = parse_positive_int(
        args[0],
        "num_countries must be a positive integer (e.g., top_countries 5)"
    )
    if num_countries is None:
        return

    country_counts = Counter(get_all_countries(all_data))
    for country, count in country_counts.most_common(num_countries):
        print(f"{country}: {count}")


def ships_by_types_cmd(all_data, args):
    """Display how many ships exist for each TYPE_SUMMARY."""
    types = [ship.get("TYPE_SUMMARY") for ship in all_data if ship.get("TYPE_SUMMARY")]
    if not types:
        print("No ship type data found.")
        return

    type_counts = Counter(types)
    for ship_type, count in type_counts.most_common():
        print(f"{ship_type}: {count}")


def search_ship_cmd(all_data, args):
    """Search ships by partial name (case-insensitive)."""
    if not args:
        print("Usage: search_ship <partial_name>")
        return

    query = " ".join(args).strip().lower()

    matches = [
        ship for ship in all_data
        if query in (ship.get("SHIPNAME") or "").lower()
    ]

    if not matches:
        print("No ships found.")
        return

    for ship in matches:
        print(ship.get("SHIPNAME", "(no name)"))


def speed_histogram_cmd(all_data, args):
    """Create and save a histogram of ship speeds."""
    output_file = args[0] if args else "speed_histogram.png"

    speeds = []
    for ship in all_data:
        raw_speed = ship.get("SPEED")
        if raw_speed in (None, ""):
            continue
        try:
            speeds.append(float(raw_speed))
        except ValueError:
            continue

    if not speeds:
        print("No valid speed data found.")
        return

    plt.figure()
    plt.hist(speeds, bins=20)
    plt.title("Ship Speed Histogram")
    plt.xlabel("Speed")
    plt.ylabel("Number of ships")
    plt.savefig(output_file)
    plt.close()

    print(f"Saved histogram to '{output_file}'")


def draw_map_cmd(all_data, args):
    """Draw ship positions (lat/lon scatter) and save to a PNG file."""
    output_file = args[0] if args else "ships_map.png"

    latitudes = []
    longitudes = []

    for ship in all_data:
        lat, lon = get_lat_lon(ship)
        if lat is not None and lon is not None:
            latitudes.append(lat)
            longitudes.append(lon)

    if not latitudes:
        print("No valid ship locations found.")
        return

    plt.figure(figsize=(12, 6))
    plt.title("Ship Positions")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    plt.grid(True)
    plt.scatter(longitudes, latitudes, s=10, alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    plt.close()

    print(f"Map saved as '{output_file}'")


def unknown_cmd(all_data, args):
    """Fallback handler for unknown commands."""
    print("Unknown command. Type 'help' to see available commands.")


# ----------------------------
# Dispatcher
# ----------------------------
COMMANDS = {
    "help": help_cmd,
    "show_countries": show_countries_cmd,
    "top_countries": top_countries_cmd,
    "ships_by_types": ships_by_types_cmd,
    "search_ship": search_ship_cmd,
    "speed_histogram": speed_histogram_cmd,
    "draw_map": draw_map_cmd,
}

COMMANDS_HELP = {
    "help": "Show this help message",
    "show_countries": "List all ship countries (alphabetical, no duplicates)",
    "top_countries": "Show the top N countries with the most ships (usage: top_countries 5)",
    "ships_by_types": "Show how many ships exist for each ship type",
    "search_ship": "Search ships by partial, case-insensitive name (usage: search_ship disney)",
    "speed_histogram": "Generate speed histogram and save to a file (optional: speed_histogram my.png)",
    "draw_map": "Draw ship positions and save to PNG (optional: draw_map map.png)",
    "exit": "Exit the program",
}


# ----------------------------
# Main CLI loop
# ----------------------------
def run_cli(all_data):
    """Run the command loop until exit or Ctrl+C."""
    print("Welcome to the Ships CLI.")
    print("Type 'help' for commands. 'exit' to quit.")

    try:
        while True:
            user_input = input("> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                print("Exiting CLI.")
                break

            handler = COMMANDS.get(command, unknown_cmd)
            handler(all_data, args)

    except KeyboardInterrupt:
        print("\nExiting CLI.")
        sys.exit(0)


def main():
    all_data = load_data()["data"]
    run_cli(all_data)


if __name__ == "__main__":
    main()

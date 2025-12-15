from load_data import load_data

all_data = load_data()
ships = all_data["data"]

no_of_ships = ships
print(f"Number of ships are:", len(no_of_ships) )




names_of_all_ships = [ship.get("SHIPNAME") for ship in ships]
names_of_all_ships_country = [ship.get("COUNTRY") for ship in ships]
print(names_of_all_ships)
print(names_of_all_ships_country)
print(len(names_of_all_ships))

countries_without_duplicate = set(ship.get("COUNTRY") for ship in ships if ship.get("COUNTRY"))
print(f"Sorted Country Names are:", sorted(countries_without_duplicate))


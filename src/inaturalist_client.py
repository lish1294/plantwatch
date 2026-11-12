
import requests

BASE_URL = "https://api.inaturalist.org/v1"

# Reuse one HTTP session for our API requests.
session = requests.Session()

session.headers.update({
    "User-Agent": "PlantWatch/0.1 (educational project)"
})


def find_place(place_name):
    """
    Search iNaturalist for a geographic place.

    Args:
        place_name: A location such as Brooklyn.

    Returns:
        A list of matching places.
    """

    url = f"{BASE_URL}/places/autocomplete"

    params = {
        "q": place_name
    }

    response = session.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])


def main():
    """Run a test search for Brooklyn."""

    places = find_place("Brooklyn")

    if not places:
        print("No matching places found.")
        return

    print("\nMatching iNaturalist places:\n")

    for place in places:
        print(
            f"Name: {place.get('display_name')}"
            f" | ID: {place.get('id')}"
        )


if __name__ == "__main__":
    main()

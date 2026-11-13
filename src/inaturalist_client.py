
import requests

BASE_URL = "https://api.inaturalist.org/v1"

# Reuse one HTTP session for our API requests.
session = requests.Session()

session.headers.update({
    "User-Agent": "PlantWatch/0.1 (educational project)"
})


def find_place(place_name):
    """
    Search iNaturalist for a county.

    Args:
        county_name: A county name such as Kings County.

    Returns:
        A list of matching counties.
    """

    url = f"{BASE_URL}/places/autocomplete"

    params = {
        "q": place_name,
        "place_type": "County",
        "per_page": 20
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
    """Find Kings County in New York."""
    """ Find the correct Kings County place ID. : 2275
Pass that ID to the iNaturalist observations endpoint.
Filter observations to plants.
Return observations that have photographs.
Paginate through the results so we can collect multiple batches."""

    places = find_place("Kings County, NY")

    if not places:
        print("No matching places found.")
        return

    print("\nMatching iNaturalist counties:\n")

    for place in places:
        print(
            f"Name: {place.get('display_name')}"
            f" | ID: {place.get('id')}"
            f" | Type: {place.get('place_type_name')}"
        )


if __name__ == "__main__":
    main()

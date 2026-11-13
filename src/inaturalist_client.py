
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

def get_plant_observations(place_id, page=1):
    """Retrieve plant observations within a geographic place."""

    url = f"{BASE_URL}/observations"

    params = {
        "place_id": 2275,  # Kings County, NY
        "taxon_id": 47126,  # Plantae
        "has[]": "photos",
        "per_page": 30,
        "page": page
    }

    print("Requesting observations...")
    print(f"URL: {url}")
    print(f"Parameters: {params}")

    response = session.get(url, params=params, timeout=20)

    print(f"Status code: {response.status_code}")
    print(f"Request URL: {response.url}")

    response.raise_for_status()

    data = response.json()

    print(f"Response type: {type(data)}")

    if isinstance(data, dict):
        observations = data.get("results", [])
    else:
        observations = data

    print(f"Observations returned: {len(observations)}")

    return observations

def main():
    # First, identify the correct county boundary.
    place_id = 2275

    # Now retrieve plant observations in that county.
    observations = get_plant_observations(place_id)

    for observation in observations:
        taxon = observation.get("taxon") or {}
        photos = observation.get("photos") or []

        print(f"Observation ID: {observation.get('id')}")
        print(f"Plant: {taxon.get('name', 'Unknown')}")
        print(f"Date: {observation.get('observed_on')}")
        print(f"Location: {observation.get('place_guess')}")

        if photos:
            print(f"Photo: {photos[0].get('url')}")

        print("-" * 40)


if __name__ == "__main__":
    main()

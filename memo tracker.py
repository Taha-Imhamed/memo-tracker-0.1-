import phonenumbers
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode, NotAuthorizedError
import folium

# Your OpenCage API key
OPENCAGE_API_KEY = 'cb19d11c282942e69d4489337c6326d0'

def track_phone_number(phone_number):
    """
    Track the location of a phone number using OpenCage and Google Geocoder APIs.

    Args:
    phone_number (str): The phone number to track, including the country code (e.g., +14155552671)

    This function will:
    - Parse and validate the phone number.
    - Determine the country and region associated with the number.
    - Use the OpenCage Geocoding API to get latitude and longitude based on the region.
    - Create an HTML file containing a map of the location.
    """
    try:
        # Parse the phone number with phonenumbers library
        parsed_number = phonenumbers.parse(phone_number)

        # Check if the phone number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            print("Invalid phone number. Please check the number format.")
            return

        # Get the country and region information of the phone number
        country = geocoder.description_for_number(parsed_number, 'en')
        region = phonenumbers.region_code_for_number(parsed_number)  # Region code like "US", "GB", etc.

        if country:
            print(f"Phone number belongs to: Country: {country}, Region Code: {region}")
        else:
            print("Could not determine the country for this number.")
            return

        # Initialize OpenCage Geocoder
        geocoder_oc = OpenCageGeocode(OPENCAGE_API_KEY)

        # Prepare a location query combining country and region
        query = f"{country}, {region}" if region else country
        results = geocoder_oc.geocode(query)

        if results:
            # Extract latitude and longitude from the API response
            location = results[0]['geometry']
            lat, lng = location['lat'], location['lng']
            print(f"Location found: Latitude {lat}, Longitude {lng}")

            # Create a map centered at the location using Folium
            map_location = folium.Map(location=[lat, lng], zoom_start=6)

            # Add a marker on the map with a popup showing the country
            folium.Marker(location=[lat, lng], popup=f"Location: {country}").add_to(map_location)

            # Save the map as an HTML file that can be viewed in a browser
            map_location.save("phone_location_map.html")
            print("Map has been saved as 'phone_location_map.html'. Open it in a browser to view the location.")

        else:
            print("Location not found. Please check if the country and region are correct.")

    except NotAuthorizedError:
        # Catch error when the OpenCage API key is incorrect or unauthorized
        print("Error: Your OpenCage API key is not authorized. Please check your key.")
    except phonenumbers.phonenumberutil.NumberParseException:
        # Handle error if the phone number format is incorrect
        print("Error parsing the phone number. Make sure it's in the correct format (e.g., +14155552671).")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Ask the user to input a phone number, including country code (e.g., +14155552671)
    phone_number = input("Enter the phone number with country code (e.g., +14155552671): ")
    track_phone_number(phone_number)

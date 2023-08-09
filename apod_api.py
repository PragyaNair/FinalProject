'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import requests

NASA_API_KEY = 'WUorXg78ssKySjKNb5scDPO75ykADSg7HJgyxsYf' 
APOD_URL = "https://api.nasa.gov/planetary/apod"

def main():
    apod_date = date.fromisoformat(argv[1])
    apod_info_dict = get_apod_info(apod_date)
    if apod_info_dict:
        apod_url = get_apod_image_url(apod_info_dict)
        apod_image_data = image_lib.download_image(apod_url)
        image_lib.save_image_file(apod_image_data,  r'C:\temp\image.jpg')
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # Setup request parameters 
    apod_params = {
        'api_key' : NASA_API_KEY,
        'date' : apod_date,
        'thumbs' : True
    }

    # Send GET request to NASA API
    print(f'Getting {apod_date} APOD information from NASA...', end='')
    resp_msg = requests.get(APOD_URL, params=apod_params)

    # Check if the info was retrieved successfully
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Convert the received info into a dictionary 
        apod_info_dict = resp_msg.json()
        return apod_info_dict
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')    

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info

    Returns:
        str: APOD image URL
    """
    if apod_info_dict['media_type'] == 'image':
        return apod_info_dict['hdurl']
    elif apod_info_dict['media_type'] == 'video':
        # Some video APODs do not have thumbnails, so this will sometimes fail
        return apod_info_dict['thumbnail_url']

if __name__ == '__main__':
    from datetime import date
    from sys import argv
    import image_lib
    main()
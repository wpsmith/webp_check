import requests
import config


def purge(cf_zone_id):
    cf_api_key = config.get().get('CF_API_KEY')

    URL = f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/purge_cache'
    cf_headers = {"Content-Type": "Application/json", "Authorization": f"Bearer {cf_api_key}"}
    cf_data = '{"purge_everything":true}'

    try:
        response = requests.post(URL, headers=cf_headers, data=cf_data)
    except Exception as err:
        print("There was an issue calling cloudflare.")
        return False
    else:
        if response.status_code == 200 and response.json()['success']:
            print("cache has been purged.")
            return True
        else:
            print("cache has NOT been purged.")
            print(f"{response.json()}")
            return False

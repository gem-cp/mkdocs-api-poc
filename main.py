# main.py
import urllib.parse

# This is the function that will be called from your markdown files
def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    @env.macro
    def badge(badge_id: str):
        """
        Creates a markdown image for a badge from the _data/badges.yml file.
        Optionally wraps it in a link if a 'link' key is present.
        
        Usage: {{ badge('release_notes') }}
        """
        # The 'data' variable is automatically populated by the plugin
        # with the content of the _data/*.yml files.
        # The filename 'badges' becomes the key.
        if 'badges' not in env.variables['data']:
            return f"Error: _data/badges.yml not found."
            
        badge_data = env.variables['data']['badges'].get(badge_id)

        if not badge_data:
            return f"Error: Badge '{badge_id}' not found in _data/badges.yml"

        # Required fields from the YAML
        label = badge_data.get('label', '')
        message = badge_data.get('message', '')
        color = badge_data.get('color', 'lightgrey')
        
        # URL-encode the parts of the badge
        label_encoded = urllib.parse.quote(label.replace("-", "--"))
        message_encoded = urllib.parse.quote(message.replace("-", "--"))

        # Base URL
        url = f"https://img.shields.io/badge/{label_encoded}-{message_encoded}-{color}"

        # Optional query parameters
        params = {
            'style': badge_data.get('style'),
            'logo': badge_data.get('logo'),
            'logoColor': badge_data.get('logoColor')
        }
        
        # Filter out None values and build the query string
        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        if query_string:
            url += f"?{query_string}"
            
        # Create the markdown image tag
        alt_text = f"{label}: {message}"
        md_image = f'![{alt_text}]({url})'

        # If a link is provided, wrap the image in a markdown link
        if 'link' in badge_data:
            link_url = badge_data['link']
            return f'[{md_image}]({link_url})'
        else:
            return md_image
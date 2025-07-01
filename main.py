# main.py
import os
import yaml  # <-- Benötigt PyYAML
import urllib.parse

def define_env(env):
    """
    This is the hook for defining variables, macros and filters.
    """

    # --------------------------------------------------------------------------
    # MANUELLES LADEN DER DATEN AUS DEM _data ORDNER
    # Das mkdocs-macros-plugin macht dies nicht automatisch.
    # Wir fügen die Logik hier hinzu.
    # --------------------------------------------------------------------------
    env.variables['data'] = {}
    data_dir = '_data'
    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith(('.yml', '.yaml')):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Der Dateiname (ohne Endung) wird zum Schlüssel.
                    # z.B. wird aus 'badges.yml' der Schlüssel 'badges'.
                    key = os.path.splitext(filename)[0]
                    env.variables['data'][key] = yaml.safe_load(f)
    # --------------------------------------------------------------------------
    # Ende des manuellen Ladens
    # --------------------------------------------------------------------------


    @env.macro
    def badge(badge_id: str):
        """
        Creates a markdown image for a badge from the _data/badges.yml file.
        Optionally wraps it in a link if a 'link' key is present.
        
        Usage: {{ badge('release_notes') }}
        """
        # Wir machen die Prüfung sicherer mit .get(), falls 'data' oder 'badges' fehlt
        if 'badges' not in env.variables.get('data', {}):
            return "Error: _data/badges.yml not found or couldn't be loaded."
            
        badge_data = env.variables['data']['badges'].get(badge_id)

        if not badge_data:
            return f"Error: Badge '{badge_id}' not found in _data/badges.yml"

        # Required fields from the YAML
        label = badge_data.get('label', '')
        message = badge_data.get('message', '')
        color = badge_data.get('color', 'lightgrey')
        
        # URL-encode the parts of the badge
        label_encoded = urllib.parse.quote(str(label).replace("-", "--"))
        message_encoded = urllib.parse.quote(str(message).replace("-", "--"))

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
def construct_base_url():
    url_components = {
        "scheme": "https",
        "domain": "api.nasa.gov",
        "path": "neo/rest/v1/feed",
    }
    return url_components

def build_base_url(base_url_components):
    # Construct the base URL
    base_url = f"{base_url_components['scheme']}://{base_url_components['domain']}/{base_url_components['path']}"

    return base_url

BASE_URL = build_base_url(construct_base_url())

# Set the API endpoint URL and the data to send
API_URL = 'https://upshop.knapa.cz'
USER_URL = f'{API_URL}/user'
COMMIT_URL = f'{API_URL}/commit'

# Set the API key as a header
HEADER = {'x-access-token': 'dev'}

# Set the number of users/commits to create at the start
START_USERS = 0
START_COMMITS = 0

# Set proportions of user/commit creation in the loop
USER_PROPORTION = 0.05

# Retry delay in seconds
REQUEST_MIN_DELAY = 30
REQUEST_MAX_DELAY = 60 * 2
CONNECTION_DELAY = 10
TIMEOUT_DELAY = 10

# Set the API endpoint URL and the data to send
API_URL = 'http://127.0.0.1:5000'
USER_URL = f'{API_URL}/user'
COMMIT_URL = f'{API_URL}/commit'

# Set the API key as a header
HEADER = {'x-access-token': 'dev'}

# Set the number of users/commits to create at the start
START_USERS = 20
START_COMMITS = 300

# Set proportions of user/commit creation in the loop
USER_PROPORTION = 0.05

# Retry delay in seconds
REQUEST_DELAY = 5
CONNECTION_DELAY = 10
TIMEOUT_DELAY = 10

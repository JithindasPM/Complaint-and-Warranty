import requests

# Set the API URL
url = 'https://platform.fatsecret.com/rest/server.api'

# Set the Authorization token (Replace with your actual access token)
access_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOEFEREZGRjZBNDkxOUFBNDE4QkREQTYwMDcwQzE5NzNDRjMzMUUiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJFSXJkX19ha2tacWtHTDNhWUFjTUdYUFBNeDQifQ.eyJuYmYiOjE3NDA0ODkxODksImV4cCI6MTc0MDU3NTU4OSwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiJlYzQxNTY5YWU1MTA0MWVhYjU3NTMyMmE3ZjFlZDRkNyIsInNjb3BlIjpbImJhc2ljIl19.hknVcQzAAKejfHUm53G4rTx5ZJ-09mjy9WEZerPne5HPGF6TS957rc7AD6-XDjV3Vi8TVD3zTFgKnIj63ZATGzQm3J5LE-TQmYrtY1L5H4_yxAR3A6TBjL8DCeA460Bh1SnYD_uQySqBod8eAUPJFExL79wTnpQUDr-VVb4WDGwogqBcOUUOZ1p0kKlavx91LsRZkCIY3OjwacPJxZxIcVBx4l-1DN0iICuyBYHon0wJLBMpfFuyEsqem0RuBZENy0goaYPvpG6YRfuWCuVaZLUQQ2lx2wgty_S-gW-tN7YOpAEr6kuoD2AGfFGlngn7H6cWzZdqbGn8yc9IFWh_P15vhvdneH_aJVt4KFO1SzgqN3A1tm_7avJaLfm8BDIKcZYSR6d3HzGEn85WYrqfzXw3gxGgY1OSnzAN6PNq0zjHHcCyeMy7qm3cHL661hDnCWIqfVkiWKy96n8mMumxo6At9BVvnTcbJ9J45hZt64OxL_a9PqQrww9PPRSX8ZHhcrAAJ_907kRt3MBPba7Jd-ek9Ca0JpMzKsNDWdJCZiChAdjB4Nn122YxLjhcGoPzYm1Y1W7T_BkxmXzbdHqRQEtljkots6VW8dsRVqUf01bM2SRhKUWNa6tzPu3vdrdlaCbH_anuVgVVyLYJ2F1prty1qaXwrBwWEv2vkk1WxkQ'

# Set the parameters for the food search
payload = {
    'method': 'foods.search',
    'search_expression': 'toast',
    'format': 'json'
}

# Set the headers with Authorization Bearer token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")

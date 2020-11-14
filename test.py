import requests

url = 'https://raw.githubusercontent.com/rhyloo/agenda_bot/develop/notes.org'
r = requests.get(url, allow_redirects=True)

open('notes_2.org', 'wb').write(r.content)

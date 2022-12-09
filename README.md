# vpnclientplus
**vpnclientplus** is a multi protocol vpn client to keep your vpn always *on*, for linux and written in django.

## Features
- Add multiple configuration per each vpn protocol
- On/Off vpn enabled wifi hotspot
- Support Openvpn, Cisco, Shadowsocks, L2tp
- Simple web UI

## Development
1. `python3 -m venv env`
2. `source env/bin/activate` - On Windows use `env\Scripts\activate`
3. `pip install -r requirments.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

- creating user
  - `python manage.py createsuperuser`

## TODO
- amin
  - add turn on hotspot button
  - remove user and group section
  - better UI
  - better logic

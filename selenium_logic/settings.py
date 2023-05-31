
import requests
from config import PROF_INFO


def make_request():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    data = {
        'action': 'login',
        'username': PROF_INFO.get('username'),
        'password': PROF_INFO.get('password')
    }
    login_url = 'https://kaspi.kz/mc/api/login'

    session.post(
        url=login_url,
        headers=headers,
        data=data
    )

    return session

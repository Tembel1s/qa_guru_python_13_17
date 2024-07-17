from jsonschema import validate
import requests
from schemas import get_users, get_single_user, post_user, put_user, register_unsuccessful

endpoint = 'api/users/'
endpoint_register = 'api/register'

def test_all_users_should_have_email_field(url):
    response = requests.get(f'{url}{endpoint}')
    body = response.json()
    emails = [element['email'] for element in body['data']]

    assert response.status_code == 200
    assert all('@' in email for email in emails)
    validate(body, schema=get_users)

def test_get_user_by_id(url):
    id = '6'
    response = requests.get(f'{url}{endpoint}{id}')
    body = response.json()

    assert response.status_code == 200
    assert body['data']['id'] == int(id)
    validate(body, schema=get_single_user)


def test_get_user_by_id_not_found(url):
    id = '13'
    response = requests.get(f'{url}{endpoint}{id}')
    body = response.json()

    assert response.status_code == 404
    assert body == {}


def test_create_user_should_return_id(url):
    name = 'Mr. Proper'
    job = 'Cleaner'
    payload = {'name': name, 'job': job}
    response = requests.post((f'{url}{endpoint}'), json=payload)
    body = response.json()

    assert response.status_code == 201
    assert 'id' in body
    validate(body, schema=post_user)


def test_update_user_successful(url):
    name = 'Mr. Proper'
    job = 'Cleaner'
    id = '2'
    payload = {'name': name, 'job': job}
    response = requests.put(f'{url}{endpoint}{id}', json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=put_user)


def test_delete_user(url):
    id = '2'
    response = requests.delete(f'{url}{endpoint}{id}')

    assert response.status_code == 204
    assert response.text == ''


def test_register_unsuccessful(url):

    payload = {
        "email": "mr@proper"
    }
    response = requests.post((f'{url}{endpoint_register}'),json=payload)
    body = response.json()

    assert response.status_code == 400
    validate(body, schema=register_unsuccessful)




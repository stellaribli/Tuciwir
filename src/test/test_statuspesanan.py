import requests


def test_review_diproses_():
    tuteers_id = 1
    item = requests.get('https://tuciwir.azurewebsites.net/reviewdiproses?tuteers_id={}'.format(tuteers_id))
    assert item.status_code == 200


def test_review_done():
    tuteers_id = 1
    item = requests.get('https://tuciwir.azurewebsites.net/reviewdone?tuteers_id={}'.format(tuteers_id))
    assert item.status_code == 200
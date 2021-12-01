import requests


def test_lihat_review():
    id_reviewer = 1
    url = 'https://tuciwir.azurewebsites.net/reviewerbookingdia?id_reviewer='
    item = requests.get(url + str(id_reviewer))

    assert item.status_code == 200

def test_reviewer_pilih_booking_fail():
    id_reviewer = 1
    id_booking = 1
    url = 'https://tuciwir.azurewebsites.net/reviewerpilihbooking?id_booking='
    item = requests.post(url + str(id_booking) + '&id_reviewer=' + str(id_reviewer))
    
    assert item.status_code == 500

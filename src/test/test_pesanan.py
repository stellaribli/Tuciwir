import requests


def test_create_booking_success():
    paket_id = 1
    tuteers_id = 35
    url = 'http://tuciwir.azurewebsites.net/create-booking?paket_id=' + str(paket_id) + '&tuteers_id=' + str(tuteers_id)
    response = requests.post(url)
    assert response.status_code == 200

def test_create_booking_fail():
    paket_id = 5
    tuteers_id = 35
    url = 'http://tuciwir.azurewebsites.net/create-booking?paket_id=' + str(paket_id) + '&tuteers_id=' + str(tuteers_id)
    response = requests.post(url)
    assert response.status_code == 404

def test_create_transaksi_success():
    booking_id = 1
    url = 'http://tuciwir.azurewebsites.net/create-transaksi?booking_id=' + str(booking_id)
    response = requests.post(url)
    assert response.status_code == 200


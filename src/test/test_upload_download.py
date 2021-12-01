import requests


def test_download_cv_success():
    booking_id = 2
    url = "https://tuciwir.azurewebsites.net/download-cv?booking_id=" + str(booking_id)
    response = requests.get(url)
    assert response.status_code == 200

def test_download_cv_fail():
    booking_id = 4
    url = "https://tuciwir.azurewebsites.net/download-cv?booking_id=" + str(booking_id)
    response = requests.get(url)
    assert response.status_code == 200

def test_download_review_success():
    booking_id = 2
    url = "https://tuciwir.azurewebsites.net/download-cv-review?booking_id=" + str(booking_id)
    response = requests.get(url)
    assert response.status_code == 200

def test_download_review_fail():
    booking_id = 4
    url = "https://tuciwir.azurewebsites.net/download-cv-review?booking_id=" + str(booking_id)
    response = requests.get(url)
    assert response.status_code == 404

# def test_upload_cv_success():
#     booking_id = 2
#     url = "https://tuciwir.azurewebsites.net/upload-cv?booking_id=" + str(booking_id)
#     response = requests.put(url)
#     assert response.status_code == 200

# def test_upload_cv_fail():
#     booking_id = 4
#     url = "https://tuciwir.azurewebsites.net/upload-cv?booking_id=" + str(booking_id)
#     response = requests.put(url)
#     assert response.status_code == 404


# def test_upload_review_success():
#     booking_id = 2
#     reviewer_id = 1
#     url = 'https://tuciwir.azurewebsites.net/upload-review?booking_id={}&reviewer_id={}'.format(booking_id, reviewer_id)
#     response = requests.put(url)
#     assert response.status_code == 200

# def test_upload_review_fail():
#     booking_id = 4
#     reviewer_id = 1
#     url = 'https://tuciwir.azurewebsites.net/upload-review?booking_id={}&reviewer_id={}'.format(booking_id, reviewer_id)
#     response = requests.put(url)
#     assert response.status_code == 404



import requests
import urllib

def test_login_tuteers_success():
    email = 'b@mbang.com'
    password = 'asdf'
    f = {'email': email, 'password': password}
    parsed = (urllib.parse.urlencode(f))
    url = 'https://tuciwir.azurewebsites.net/login?' + parsed
    hasil = requests.get(url)

    assert hasil.text == 'true'

def test_login_tuteers_fail():
    email = 'b@mbang.com'
    password = 'asdE'
    f = {'email': email, 'password': password}
    parsed = (urllib.parse.urlencode(f))
    url = 'https://tuciwir.azurewebsites.net/login?' + parsed
    hasil = requests.get(url)

    assert hasil.text == 'false'

def test_login_admin_success():
    email = 'caca@tuciwir.com'
    password = 'asdf'
    f = {'email': email, 'password': password}
    parsed = (urllib.parse.urlencode(f))
    url = 'https://tuciwir.azurewebsites.net/loginadmin?' + parsed
    hasil = requests.get(url)
    
    assert hasil.text == 'true'

def test_login_admin_fail():
    email = 'caca@tuciwir.com'
    password = 'asdE'
    f = {'email': email, 'password': password}
    parsed = (urllib.parse.urlencode(f))
    url = 'https://tuciwir.azurewebsites.net/loginadmin?' + parsed
    hasil = requests.get(url)
    
    assert hasil.text == 'false'

def test_signup_tuteers_success():
    name = 'Tutut'
    email = 'tutut@gmail.com'
    password = 'asdf'
    reenterpass = 'asdf'
    noHP = '1'
    year = '2001'
    month = '04'
    date = '12'
    gender = 'Female'

    f = {
        'name': name, 
        'email': email, 
        'password': password, 
        'reenterpass': reenterpass,
        'noHP': noHP, 
        'year': year, 
        'month': month, 
        'date': date, 
        'gender': gender
        }
    
    parsed = (urllib.parse.urlencode(f))
    url = 'https://tuciwir.azurewebsites.net/registerSQL?' + parsed
    hasil = requests.post(url)
    
    assert hasil.status_code == 200

def test_signup_tuteers_fail():
    name = 'Tutut'
    email = 'tutut@gmail.com'
    password = 'asdf'
    reenterpass = 'asdE'
    noHP = '1'
    year = '2001'
    month = '04'
    date = '12'
    gender = 'Female'

    f = {
        'name': name, 
        'email': email, 
        'password': password, 
        'reenterpass': reenterpass,
        'noHP': noHP, 
        'year': year, 
        'month': month, 
        'date': date, 
        'gender': gender
        }
    
    parsed = (urllib.parse.urlencode(f))
    url = 'https://tuciwir.azurewebsites.net/registerSQL?' + parsed
    hasil = requests.post(url)
    
    assert hasil.text == '"Password Tidak Sama!"'




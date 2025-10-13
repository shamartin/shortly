def test_environment_config(app):
    #make sure we are not touching the actual database and that nothing broke
    with app.app_context():
        assert app.config["TESTING"] is True
        assert "sqlite:///:memory:" in app.config["SQLALCHEMY_DATABASE_URI"]

def test_post_add_entry(client):
    response = client.post('/api/urls/', json={'full_url': 'https://www.totallyrealwebsite.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['short_code'] is not None
    assert data['full_url'] == 'https://www.totallyrealwebsite.com'

def test_post_add_duplicate_entry(client):
    #post URL once
    client.post('/api/urls/', json={'full_url': 'https://www.totallyrealwebsite.com'})
    #post it again!
    response = client.post('/api/urls/', json={'full_url': 'https://www.totallyrealwebsite.com'})

    assert response.status_code == 409
    data = response.get_json()
    assert data == {"message": "The requested URL has already beeen shortened. Please use this URL: http://www.shortly.com/1"}

def test_get_all_entries(client, app):
    #/api/urls with no id specified
    from shortly.models import UrlModel
    from shortly import db

    url1 = UrlModel(full_url='https://www.foo.com', short_code='ABC')
    url2 = UrlModel(full_url='https://www.bar.com', short_code='DEF')

    with app.app_context():
        db.session.add_all([url1, url2])
        db.session.commit()

    response = client.get('/api/urls/')
    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 2
    assert data == [{'full_url' : 'https://www.foo.com', 'id': 1, 'short_code':'ABC'},
                    {'full_url' : 'https://www.bar.com', 'id': 2, 'short_code':'DEF'}]

def test_get_one_entry(client, app):
    #api/urls/<id>
    from shortly.models import UrlModel
    from shortly import db

    url1 = UrlModel(full_url='https://www.foo.com', short_code='ABC')
    url2 = UrlModel(full_url='https://www.bar.com', short_code='DEF')

    with app.app_context():
        db.session.add_all([url1, url2])
        db.session.commit()

    response = client.get('/api/urls/DEF')
    assert response.status_code == 200
    data = response.get_json()

    assert data == {'full_url' : 'https://www.bar.com', 'id': 2, 'short_code':'DEF'}

def test_get_one_entry_fail(client):
    #entry does not exist case
    response = client.get('/api/urls/123')#db is empty-- we are searching for something that does not exist

    assert response.status_code == 404
    data = response.get_json()

    assert data == {"message": "The requested URL could not be found"}

def test_search_and_redirect(client, app):
    from shortly.models import UrlModel
    from shortly import db
    url = UrlModel(full_url='https://www.foo.com', short_code='ABC')

    with app.app_context():
        db.session.add(url)
        db.session.commit()

    response = client.get('/ABC', follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == "https://www.foo.com"

def test_search_and_redirect_fail(client):
    response = client.get('/DEF', follow_redirects=False) # this does not exist in DB

    assert response.status_code == 404
    data = response.get_json()
    assert data == {"message": "The requested URL could not be found"}
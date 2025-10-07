def test_post_add_entry(client):
    response = client.post('/api/urls/', json={'full_url': 'https://www.totallyrealwebsite.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['short_code'] is not None
    assert data['full_url'] == 'https://www.totallyrealwebsite.com'

#TODO: functionality needs to be added for this edge case
#def test_post_add_duplicate_entry(client):

def test_get_all_entries(client, app):
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


def test_get_one_entry_fail(client, app):
    #entry does not exist case
    from shortly.models import UrlModel
    from shortly import db

    url1 = UrlModel(full_url='https://www.foo.com', short_code='ABC')
    url2 = UrlModel(full_url='https://www.bar.com', short_code='DEF')

    with app.app_context():
        db.session.add_all([url1, url2])
        db.session.commit()

    response = client.get('/api/urls/123')#db is empty-- we are searching for something that does not exist

    assert response.status_code == 404
    data = response.get_json()

    assert data == {"message": "The requested URL could not be found"}


import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def app():
    app = import_app('app')  # assumes your app file is named app.py
    yield app

def test_header(dash_duo, app):
    dash_duo.start_server(app)
    header = dash_duo.find_element('h1')
    assert header is not None
    assert 'Pink Morsel' in header.text

def test_visualisation_present(dash_duo, app):
    dash_duo.start_server(app)
    graph = dash_duo.find_element('#sales-3d-chart')
    assert graph is not None

def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)
    region_picker = dash_duo.find_element('#region-selector')
    assert region_picker is not None

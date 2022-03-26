import pytest
from app import *
read_data_from_file_into_dict()

def test_help():
    assert isinstance(help(),str)==True

def test_get_all_epochs():
    assert isinstance(get_all_epochs(),str)==True

def test_get_epoch_data():
    assert isinstance(get_epoch_data('randomword'),dict)==True

def test_get_all_countries():
    assert isinstance(get_all_countries(),dict)==True

def test_get_country_data():
    assert isinstance(get_country_data('randomword'),str)==True

def test_get_all_regions():
    assert isinstance(get_all_regions('randomword'),dict)==True

def test_get_region_data():
    assert isinstance(get_region_data('randomword', 'randomword'),str)==True

def test_get_all_cities():
    assert isinstance(get_all_cities('randomword','randomword'),dict)==True

def test_get_city_data():
    assert isinstance(get_city_data('randomword','randomword','randomword'),str)==True

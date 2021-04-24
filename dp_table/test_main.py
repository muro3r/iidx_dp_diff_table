import pytest
import requests
import requests_mock
from bs4 import BeautifulSoup
from dp_table import main


def test_sample(test_data, requests_mock: requests_mock):
    requests_mock.get('https://zasa.sakura.ne.jp/dp/run.php', text=test_data)

    assert isinstance(
        main.download_unofficial_difficulty_table(), BeautifulSoup,
    )


def test_parse_difficulty_table(test_data: str):
    bs = BeautifulSoup(test_data, features='html.parser')
    result = main.parse_unofficial_difficulty_table(bs)

    assert len(result) == 1
    assert result[0].title == '22DUNK'
    assert result[0].hyper.official_difficulty == 5
    assert result[0].hyper.unofficial_difficulty == 5.9

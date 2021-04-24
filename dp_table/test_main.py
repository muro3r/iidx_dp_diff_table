import math

from bs4 import BeautifulSoup

from dp_table import main


def test_sample(test_data, requests_mock):
    requests_mock.get('https://zasa.sakura.ne.jp/dp/run.php', text=test_data)

    assert isinstance(
        main.download_unofficial_difficulty_table(), BeautifulSoup,
    )


def test_parse_difficulty_table(test_data: str):
    bs = BeautifulSoup(test_data, features='html.parser')
    songs = main.parse_unofficial_difficulty_table(bs)

    song = songs[0]
    assert len(songs) == 1
    assert song.title == '22DUNK'

    assert song.hyper.official_difficulty == 5
    assert math.isclose(song.hyper.unofficial_difficulty, 5.9)

    assert song.another.official_difficulty == 5
    assert math.isclose(song.another.unofficial_difficulty, 6.5)


def test_dump():
    song = main.Song()
    song.title = 'song title'

    song.hyper = main.Difficulty(7, 7.8)

    main.dump_difficultiy_table([song])

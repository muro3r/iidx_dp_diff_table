from dataclasses import dataclass
import re
import requests
from bs4 import BeautifulSoup
from bs4 import element


@dataclass
class Difficulty:
    official_difficulty: int
    unofficial_difficulty: float

    def __post_init__(self):
        self.official_difficulty = int(self.official_difficulty)
        self.unofficial_difficulty = float(self.unofficial_difficulty)


class Song:
    title: str
    hyper: Difficulty
    another: Difficulty
    leggendaria: Difficulty


def download_unofficial_difficulty_table() -> BeautifulSoup:
    response = requests.get('https://zasa.sakura.ne.jp/dp/run.php')
    response.raise_for_status()

    return BeautifulSoup(response.text, features='html.parser')


def parse_unofficial_difficulty_table(bs: BeautifulSoup) -> list[Song]:
    rows = bs.find_all('tr')

    result = []

    row: 'element.Tag'
    for row in rows:
        song_title = row.select_one('td.music')
        if not song_title:
            continue

        song = Song()
        song.title = song_title.text

        datum = row.find_all('td')

        m = re.match(r'^\n☆(\d+) \((\d{1,}\.\d)\)\n$', datum[0].text)
        if not m:
            continue
        o_diff, uno_diff = m.groups()

        song.hyper = Difficulty(o_diff, uno_diff)

        result.append(song)

    return result


if __name__ == '__main__':

    pass

import json
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, element


@dataclass
class Difficulty:
    official_difficulty: int
    unofficial_difficulty: float


class Song:
    hyper: Difficulty
    another: Difficulty
    leggendaria: Difficulty
    title: str


def download_unofficial_difficulty_table() -> BeautifulSoup:
    response = requests.get('https://zasa.sakura.ne.jp/dp/run.php')
    response.raise_for_status()

    return BeautifulSoup(response.text, features='html.parser')


def parse_unofficial_difficulty_table(bs: BeautifulSoup) -> list[Song]:
    rows = bs.find_all('tr')

    songs: list[Song] = []

    pattern = re.compile(r'☆(\d+)\s\((\d{1,}\.\d+)\)')
    difficulties = ['hyper', 'another', 'legenddaria']
    row: 'element.Tag'
    for row in rows:
        song_title = row.select_one('td.music')
        if not song_title:
            continue

        song = Song()
        song.title = song_title.text

        cells = row.find_all('td')

        for num, diff in enumerate(difficulties):
            match = re.match(pattern, cells[num].text)

            if not match:
                continue

            o_diff, uno_diff = match.groups()
            o_diff = int(o_diff)
            uno_diff = float(uno_diff)
            setattr(song, diff, Difficulty(o_diff, uno_diff))

        songs.append(song)

    return songs


def dump_difficultiy_table(songs: list[Song]) -> None:
    text = [song.__dict__ for song in songs]

    with open('out.json', 'w') as f:
        f.write(json.dumps(text, default=lambda o: o.__dict__, ensure_ascii=False))


if __name__ == '__main__':
    bs = download_unofficial_difficulty_table()

    songs = parse_unofficial_difficulty_table(bs)

    dump_difficultiy_table(songs)

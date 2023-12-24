import argparse
import yaml
import jsonpickle
import random
import feedparser
from dataclasses import dataclass

@dataclass
class Feed:
    url: str
    title: str = None
    icon: str = None
    frequency: int = 1

    def shouldUpdate(self):
        f = self.frequency * 2
        return random.randint(1, f) == 1

    def lastArticle(self):
        try:
            f = feedparser.parse(self.url)
            e = f.entries[0]
            t = f.feed.title
            if not t:
                t = self.title
            if not e.title:
                e.title = self.title
            return Post(e.link, self.icon, t, e.title)
        except:
            print(self.url)
            return None


@dataclass
class Post:
    link: str
    icon: str
    site: str
    title: str

    def print(self):
        output = f'<div class="story"><span class="fa fa-fw {self.icon}"></span><span class="title"><a href="{self.link}">{self.title}</a></span><i class="feed">{self.site}</i></div>'
        return output


def write_page(state):
    for p in state['posts'][::-1]:
        print(p.print())


def save_to_json_pickle(filename, data):
    with open(filename, 'w') as file:
        json_data = jsonpickle.encode(data)
        file.write(json_data)

def load_json_pickle(filename):
    try:
        with open(filename, 'r') as file:
            json_data = file.read()
            data = jsonpickle.decode(json_data)
            return data
    except:
        return {'last': {}, 'posts': []}


def parse_yaml_file(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        return data

def main():
    parser = argparse.ArgumentParser(description="Update RSS feeds")
    parser.add_argument("feeds", help="Path to feeds file")
    parser.add_argument("db", help="Path to db file")
    args = parser.parse_args()

    feedlist = parse_yaml_file(args.feeds)
    state = load_json_pickle(args.db)

    feeds = []

    for f in feedlist:
        feeds.append(Feed(f.get('url', None), f.get('title', None), f.get('icon', None), f.get('freq', 1)))

    for f in feeds:
        if f.shouldUpdate():
            p = f.lastArticle()

            if not p:
                continue

            if state['last'].get(f.url, None) == p:
                continue

            state['last'][f.url] = p
            state['posts'].append(p)

    if len(state['posts']) > 200:
        state['posts'] = state['posts'][-200:]

    save_to_json_pickle(args.db, state)
    write_page(state)


if __name__ == "__main__":
    main()

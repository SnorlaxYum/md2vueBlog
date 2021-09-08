from datetime import datetime
from feedgen.feed import FeedGenerator
from pytz import timezone
from conf import SITEURL, FEEDAUTHOR
from urllib.parse import urljoin
from os import makedirs
from os.path import dirname

TZ = timezone("Asia/Chongqing")


class AtomGen(FeedGenerator):
    def __init__(self, title, description, link, language):
        super().__init__()
        self.title(title)
        self.description(description)
        self.author(FEEDAUTHOR)
        self.id(link)
        self.link(href=SITEURL, rel='alternate')
        self.link(href=link, rel='self')
        self.language(language)

    def entry_add(self,
                  titl,
                  link,
                  published,
                  updated='',
                  content='',
                  order='append'):
        entry = super().add_entry(order=order)
        # print(entry)
        entry.title(titl)
        entry.link(href=link)
        if content:
            entry.content(content)
        entry.id(link)
        # print("published: "+published)
        # print("updated: "+updated)
        entry.published(TZ.localize(
            datetime.strptime(published, '%Y-%m-%d %H:%M')))
        entry.updated(TZ.localize(
            datetime.strptime(published, '%Y-%m-%d %H:%M')))
        if updated:
            entry.updated(TZ.localize(
                datetime.strptime(updated, '%Y-%m-%d %H:%M')))
        return entry

    def atom_file(self, path):
        makedirs(dirname(path), exist_ok=True)
        super().atom_file(path)


def addEntryToFeed(post, feed, date, modified=''):
    """add a post to posts feed"""
    post_entry_url = urljoin(SITEURL, post['slug'])
    
    post_entry = feed.entry_add(
        post['title'], post_entry_url, date, modified, post['summary'])
    return post_entry

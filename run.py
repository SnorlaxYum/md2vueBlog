from functools import cmp_to_key
import os
from slugify import slugify
from json import dumps
import collections
from urllib.parse import urlparse, urljoin
from time import time

from md import markdownOpen, formatMdMeta
from vue import getTemp, writeToVue
from atom import AtomGen, addEntryToFeed
from conf import SITENAME, SITEURL, post_output_directory, static_dir, cat_feed_slug_path_format, cat_feed_path_format, contents_dir, tag_temp_file, tags_temp_file, post_temp_file, cat_temp_file, tags_feed_slug, tags_slug
from posts import sortmethod

posts = {}
posts_all = []
posts_pubDate = {}
posts_modDate = {}
post_slugs = []
tags = {}
cat_feeds = {}
postsCatYear = {}
postsCatYearMonth = {}
postsCatYearMonthDay = {}


def posts_meta(directory):
    """Deal with the posts"""
    # list markdown directory
    cats = os.listdir(directory)
    for cat in cats:
        # Add cat to 3 post dicts too
        postsCatYear[cat] = {}
        postsCatYearMonth[cat] = {}
        postsCatYearMonthDay[cat] = {}
        posts[cat] = []

        cat_slug = slugify(cat)
        cat_path = os.path.join(directory, cat)
        cat_write_path = os.path.join(post_output_directory, cat_slug)
        os.makedirs(cat_write_path, exist_ok=True)
        cat_posts = os.listdir(cat_path)
        # initiate feed for the category
        cat_id = urljoin(SITEURL, cat_slug)
        cat_feeds[cat] = AtomGen(
            "%s - %s" % (cat, SITENAME),
            "%s in %s" % (cat, SITENAME), cat_id, 'en')
        for post in cat_posts:
            if not post.endswith('.md'):
                continue
            md = markdownOpen()
            content = open(os.path.join(cat_path, post),
                           encoding='utf-8-sig').read()
            content_html = md.convert(content)
            rep_index = 0

            content_meta = formatMdMeta(md.Meta, cat_slug, cat, content_html)

            while content_meta['slug'] in post_slugs:
                rep_index += 1
                content_meta['slug'] = '{}-{}'.format(content_meta['slug'].rstrip('/'), rep_index)

            post_slugs.append(content_meta['slug'].rstrip('/'))
            posts_all.append(content_meta)
            for tag in content_meta['tags']:
                if not tag[1] in tags:
                    tags[tag[1]] = {'name': tag[0], 'posts': []}


def tags_files(tags):
    # tags json and atom generation
    # sort the tags by post count in a descending order
    tags = collections.OrderedDict(
        sorted(tags.items(), key=lambda kv: -len(kv[1]['posts'])))
    tags_list = {}
    # init feed for tags
    tags_feed_path = os.path.join(static_dir, tags_feed_slug)
    tags_id = urljoin(SITEURL, tags_slug)
    tags_feed = AtomGen("Tags - %s" %
                        SITENAME, "The tags in %s" % SITENAME, tags_id, 'en')

    for tag, tag_things in tags.items():
        # dump to tags_list
        tags_list[tag_things['name']] = {
            'length': len(tag_things['posts']), 'slug': tag}
        # Add the tag to the total tags feed
        tag_entry_url = urljoin(SITEURL, tag)
        # print(tags[tag]['posts'], "Pub: "+tags[tag]['posts'][-1]['date'])
        tags_feed.entry_add(
            tag_things['name'],
            tag_entry_url, posts_pubDate[tags[tag]['posts'][-1]['slug']],
            posts_modDate[tags[tag]['posts'][0]['slug']])

        # parsepostdates(tags[tag])
        # {
        #     "name": string,
        #     "posts": [
        #         {
        #         "title": string,
        #         "date": string,
        #         "author": string,
        #         "tags": [
        #             ["golang", "/tags/golang"],
        #             ["angular", "/tags/angular"]
        #         ],
        #         "summary": string,
        #         "slug": string
        #         }
        #     ]
        # }
        tagPath = os.path.join(post_output_directory, "{}.vue".format(tag.strip('/')))
        tagData = tags[tag]
        tagContent = getTemp(tag_temp_file).replace('{data}', dumps(tagData))
        writeToVue(tagPath, tagContent)
        print("Wrote to {}".format(tagPath))

    # tags atom generation
    tags_feed.atom_file(tags_feed_path)
    print("Wrote to %s" % tags_feed_path)

    # tags
    # {"atom": "https://snorl.ax/tags/atom.xml", "tags": {"isso": {"length": 4, "slug": "/tags/isso"},}}

    tagsPathNow = os.path.join(post_output_directory, 'tags', 'index.vue')
    tagsContent = getTemp(tags_temp_file).replace('{data}', dumps(
        {'atom': urljoin(SITEURL, tags_feed_slug), 'tags': tags_list}))

    writeToVue(tagsPathNow, tagsContent)

    print("Wrote to {}".format(tagsPathNow))


# TODO: content_meta = posts_all
# TODO: posts[cat].append(content_meta)
# TODO: tags[tag[1]]['posts'].append(content_meta)
def posts_files(posts_all):
    # sort all posts
    posts_all = sorted(posts_all, key=cmp_to_key(sortmethod))

    # add posts to posts, tags and time dicts
    for post in posts_all:
        # simple summaries
        categoryNow = post['category']
        yearNow = post['post_year']
        monthNow = post['post_month']
        dayNow = post['post_day']
        slugNow = post['slug']
        postSimple = {
            "title": post['title'],
            "date": post['date_parsed'],
            "author": post['author'],
            "tags": post['tags'],
            "summary": post['summary'],
            "slug": slugNow
        }

        posts_pubDate[slugNow] = post['date']
        posts_modDate[slugNow] = ''

        if 'modified_parsed' in post:
            postSimple['modified'] = post['modified_parsed']
            posts_modDate[slugNow] = post['modified']

        # add to posts (cat dict)
        posts[categoryNow].append(postSimple)
        # tags (tag dict)
        for tag in post['tags']:
            tags[tag[1]]['posts'].append(postSimple)
        # time dicts
        yearKey = '{}'.format(yearNow)
        monthKey = '{}/{}'.format(yearNow, monthNow)
        dayKey = '{}/{}/{}'.format(yearNow, monthNow, dayNow)
        if yearKey not in postsCatYear[categoryNow]:
            postsCatYear[categoryNow][yearKey] = []

        if monthKey not in postsCatYearMonth[categoryNow]:
            postsCatYearMonth[categoryNow][monthKey] = []

        if dayKey not in postsCatYearMonthDay[categoryNow]:
            postsCatYearMonthDay[categoryNow][dayKey] = []

        postsCatYear[categoryNow][yearKey].append(postSimple)
        postsCatYearMonth[categoryNow][monthKey].append(postSimple)
        postsCatYearMonthDay[categoryNow][dayKey].append(postSimple)

        # inside
        # {
        # "title": "A mania you can't miss",
        # "date": "January 23, 2018",
        # "tags": [
        #     ["Fall Out Boy", "/tags/fall-out-boy"],
        #     ["M A N I A", "/tags/m-a-n-i-a"]
        # ],
        # "author": "Sim",
        # "summary": "Ready for a mania?",
        # "ogimage": ["/images/og/fobmania-twitter.png"],
        # "slug": "/browser/2018/01/23/a-mania-you-can-t-miss/",
        # "html": "<p><img alt=\"mania\" src=\"https://static.snorl.ax/posts/fobmania.jpg\" title=\"Album Cover\"><br><strong>On January 18,</strong><br>Mania, Fall Out Boy's new studio album, was released on Google Play Music one day ahead of the release date of the Audio CD form.<br>The music video of a album track, \"Church\", was released on Youtube.<br><iframe class=\"youtube\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" src=\"https://www.youtube.com/embed/l3vbvF8bQfI\" frameborder=\"0\"></iframe><br>Previously released music video from the album:<br><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/VtVFTuIZFYU\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/JJJpRl2cTJc\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/7YAAyUFL1GQ\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/jG1JY0rt2Os\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/wH-by1ydBTM\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe></p>\n<p><strong>On January 19,</strong><br>The audio CD form was released. And they did a LIVE on Good Morning America.<br><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/Fjr1420IndY\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/PRLa_q13PgE\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe></p>\n<p><strong>On January 22,</strong><br>Fall Out Boy released the video where Patrick did the magic nerd stuff about \"Church\" on Twitter.<br></p>\n<blockquote class=\"twitter-video\" data-lang=\"en\"><p lang=\"en\" dir=\"ltr\">The voice of an \ud83d\udc7c watch back when Patrick was in the studio recording vocal takes for Church <a href=\"https://twitter.com/hashtag/blessed?src=hash&amp;ref_src=twsrc%5Etfw\">#blessed</a> <a href=\"https://twitter.com/hashtag/nerdstuff?src=hash&amp;ref_src=twsrc%5Etfw\">#nerdstuff</a> <a href=\"https://twitter.com/hashtag/FOBMANIA?src=hash&amp;ref_src=twsrc%5Etfw\">#FOBMANIA</a> <a href=\"https://t.co/GpbaogM9Zv\">pic.twitter.com/GpbaogM9Zv</a></p>&mdash; Fall Out Boy (@falloutboy) <a href=\"https://twitter.com/falloutboy/status/955612181751574528?ref_src=twsrc%5Etfw\">January 23, 2018</a></blockquote>\n<script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>\n<p>Pete Wentz did a LIVE with the album music played while bathing and doing some Q&amp;A.<br></p>\n<blockquote class=\"twitter-tweet\" data-lang=\"en\"><p lang=\"und\" dir=\"ltr\"><a href=\"https://t.co/U9jm3hqX4i\">https://t.co/U9jm3hqX4i</a></p>&mdash; pw (@petewentz) <a href=\"https://twitter.com/petewentz/status/955563045715144706?ref_src=twsrc%5Etfw\">January 22, 2018</a></blockquote>\n<script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>\n<p>Buy a copy if u haven't done that! You can't miss the mania!<br>I have been listenin' to the whole album like hundreds of times since buying one on Google Play Music!</p>",
        # "category": "Browser"
        # }
        infoNow = post
        pathNow = os.path.join(post_output_directory, '.'+infoNow['slug'], 'index.vue')
        if 'modified' in infoNow:
            modi = infoNow['modified_parsed']
        else:
            modi = ''
        if 'ogimage' in infoNow:
            ogimage = infoNow['ogimage']
        else:
            ogimage = '/images/og/default.webp'

        post_temp = getTemp(post_temp_file)

        content = post_temp.replace(
            '{data}',
            dumps(
                {'title': infoNow['title'],
                 'date': infoNow['date_parsed'],
                 'modified': modi, 'tags': infoNow['tags'],
                 'slug': infoNow['slug'],
                 'category': infoNow['category'],
                 'links': infoNow['links'],
                 'ogimage': ogimage, 'summary': infoNow['summary']})).replace(
            '{html}', infoNow['html'])

        writeToVue(pathNow, content)

        print("Wrote to {}".format(pathNow))

    # write to category
    for cat, cat_posts in posts.items():
        cat_slug = slugify(cat)
        # Add the recent 5 posts to the total cat feed
        recent_po = posts[cat][:5]
        for post in recent_po:
            addEntryToFeed(post, cat_feeds[cat], posts_pubDate[post['slug']], posts_modDate[post['slug']])
        # cat rss generation
        cat_feed_slug_path = cat_feed_slug_path_format % cat_slug
        cat_feed_path = cat_feed_path_format % cat_slug
        cat_feeds[cat].atom_file(cat_feed_path)
        print("Wrote to %s" % (cat_feed_path))
        # cat
        # {
        #     "name": "Browser",
        #     "atom": "https://snorl.ax/browser/atom.xml",
        #     "posts": [
        #         {
        #         "title": "NetEase went under fire for treatment of ill employee",
        #         "date": "November 25, 2019",
        #         "author": "Sim",
        #         "tags": [
        #             ["Netease", "/tags/netease"],
        #             ["employment", "/tags/employment"]
        #         ],
        #         "summary": "Recently NetEase went under fire for treatment of ill employee",
        #         "slug": "/browser/2019/11/25/netease-went-under-fire-for-treatment-of-ill-employee/"
        #         },
        #     ]
        # }
        catPath = os.path.join(post_output_directory, '{}/index.vue'.format(cat_slug))
        catData = {'name': cat, 'atom': urljoin(
            SITEURL, cat_feed_slug_path), 'posts': posts[cat]}
        catContent = getTemp(cat_temp_file).replace('{data}', dumps(catData))
        writeToVue(catPath, catContent)

        print("Wrote to {}".format(catPath))

    # Add the recent 5 posts to the total cat feed
    all_recent = posts_all[:5]
    for post in all_recent:
        addEntryToFeed(post, all_feed, posts_pubDate[post['slug']], posts_modDate[post['slug']])
    # rss generation for recent posts
    all_feed_path = os.path.join(static_dir, 'atom.xml')
    all_feed.atom_file(all_feed_path)
    print("Wrote to %s" % all_feed_path)

a = time()

all_feed = AtomGen('Recent posts in %s' %
                   SITENAME, 'Recent posts in %s' % SITENAME, SITEURL, 'en')
posts_meta(contents_dir)
posts_files(posts_all)
tags_files(tags)
b = time()

print('generation done in {} seconds'.format(b-a))
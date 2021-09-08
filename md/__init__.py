import markdown
from slugify import slugify
from conf import tag_slug_format, post_slug_format
from posts import parseGivenDate
from datetime import datetime


def markdownOpen():
    return markdown.Markdown(extensions=['pymdownx.superfences',
                                         'pymdownx.tabbed',
                                         'meta',
                                         'footnotes',
                                         'toc',
                                         #    'codehilite',
                                         'pymdownx.highlight',
                                         'attr_list',
                                         'pymdownx.emoji',
                                         'pymdownx.extra',
                                         'pymdownx.tilde',
                                         'pymdownx.smartsymbols',
                                         'tables',
                                         'nl2br'],
                             extension_configs={
        'pymdownx.highlight': {
            'linenums': True,
            'linenums_style': 'pymdownx-inline',
            'guess_lang': True
        },
        'pymdownx.superfences':
        {'disable_indented_code_blocks': True}})


def formatMdMeta(mdMeta, cat_slug, cat, content_html):
    content_meta = mdMeta
    content_meta['title'] = "".join(content_meta['title'])
    content_meta['date'] = "".join(content_meta['date'])
    content_meta['cat_slug'] = cat_slug

    if (len(content_meta["tags"]) == 1):
        content_meta['tags'] = content_meta['tags'][0].split(', ')
    for index in range(len(content_meta['tags'])):
        content_meta['tags'][index] = [content_meta['tags'][index],
                                       tag_slug_format.format(
                                       slug=slugify(content_meta['tags'][index])
                                       ).rstrip('/')]
    if 'modified' in content_meta:
        content_meta['modified'] = "".join(content_meta['modified'])
        content_meta['modified_parsed'] = parseGivenDate(datetime.strptime(content_meta['modified'], '%Y-%m-%d %H:%M'))
    if 'author' in content_meta:
        content_meta['author'] = "".join(content_meta['author'])
    content_meta['summary'] = "".join(content_meta['summary'])
    if 'slug' in content_meta:
        content_meta['slug'] = "".join(content_meta['slug'])
    else:
        content_meta['slug'] = slugify(content_meta['title'])

    post_date = datetime.strptime(
        content_meta['date'], '%Y-%m-%d %H:%M')
    content_meta['date_parsed'] = parseGivenDate(post_date)
    content_meta['post_year'] = post_date.year
    content_meta['post_month'] = '%02d' % post_date.month
    content_meta['post_day'] = '%02d' % post_date.day
    content_meta['slug'] = post_slug_format.format(
        cat=cat_slug, year=content_meta['post_year'],
        month=content_meta['post_month'],
        day=content_meta['post_day'],
        slug=content_meta['slug'])
    # do the extra for the inside of the post
    content_meta['html'] = content_html
    content_meta['category'] = cat

    return content_meta
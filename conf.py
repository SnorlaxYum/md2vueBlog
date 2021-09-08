from os.path import join, dirname

SITENAME = "Simputer"
SITEURL = "https://snorl.ax"
FEEDAUTHOR = {'name': 'Sim', 'email': 'sim@snorl.ax'}
CURDIR = dirname(__file__)
post_output_directory = join(CURDIR, '../pages')
static_dir = join(CURDIR, '../static')
contents_dir = join(CURDIR, '../contents')
cat_temp_file = join(CURDIR, 'template/_cat/index.vue')
tag_temp_file = join(CURDIR, 'template/tags/_tag.vue')
tags_temp_file = join(CURDIR, 'template/tags/index.vue')
post_temp_file = join(CURDIR, 'template/_cat/_year/_month/_day/_slug.vue')
cat_feed_slug_path_format = './%s/atom.xml'
cat_feed_path_format = join(static_dir, cat_feed_slug_path_format)
post_slug_format = "/{cat}/{year}/{month}/{day}/{slug}/"
tag_slug_format = "/tags/{slug}/"
tags_slug = '/tags'
tags_feed_slug = 'tags/atom.xml'

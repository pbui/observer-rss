#!/usr/bin/env python3

import datetime
import email
import html 
import re
import requests

# Constants

ARTICLE_RX = r'<article.*?>.*?<a href="([^"]+)" title="([^"]+)">.*?<span class="dateline">([^<]+)</span>.*?</article>'
SECTIONS   = (
    'https://www.ndsmcobserver.com/section/news',
    'https://www.ndsmcobserver.com/section/sports',
    'https://www.ndsmcobserver.com/section/scene',
    'https://www.ndsmcobserver.com/section/viewpoint',
)
HEADERS    = {
    'User-Agent': 'observer-rss',
}

# Functions

def scrape_section(url):
    response  = requests.get(url, headers=HEADERS)
    html_text = response.text.replace('\n', '')

    for link, title, dateline in re.findall(ARTICLE_RX, html_text): 
        # https://stackoverflow.com/questions/31991435/why-time-strptimesept-30-2014-b-d-y-not-working
        dateline = dateline.replace('Sept', 'Sep')
        try:
            pub_date = datetime.datetime.strptime(dateline, "%A, %B %d, %Y")
        except ValueError:
            pub_date = datetime.datetime.strptime(dateline, "%A, %b. %d, %Y")

        yield {
            'title'  : title,
            'link'   : link,
            'pubDate': email.utils.format_datetime(pub_date),
        }

def print_rss_header():
    print('''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>The Observer</title>
<link>https://www.ndsmcobserver.com/section/multimedia</link>
<description>Notre Dame / SMC Observer</description>
<atom:link href="https://yld.me/raw/ndsmcobserver-rss" rel="self" type="application/rss+xml" />
''')

def print_rss_item(article):
    print(f'''<item>
<title>{article['title']}</title>
<link>{article['link']}</link>
<pubDate>{article['pubDate']}</pubDate>
<guid isPermaLink="false">{article['link']}</guid>
</item>''')

def print_rss_footer():
    print('''</channel>
</rss>''')

# Main Execution

def main():
    print_rss_header()

    for section in SECTIONS:
        for article in scrape_section(section):
            print_rss_item(article)

    print_rss_footer()

if __name__ == '__main__':
    main()

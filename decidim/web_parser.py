import re
import html
import urllib.parse

from bs4 import BeautifulSoup

from services.downloader import Downloader


class WebParser(object):
    def get_logo_url_and_colour(url):
        contents = Downloader.get(url)

        if not contents:
            return '', ''

        try:
            htmlData = html.unescape(contents.decode('utf-8'))
            soup = BeautifulSoup(htmlData, 'html.parser')
            img = soup.select_one('div[class=logo-wrapper]').a.img
        except AttributeError:
            img = None

        if not img:
            return '', ''

        colour = None

        styles = soup.select('style')

        if len(styles) > 0:
            embedded_css = str(styles[-1])

            colour = WebParser.get_background_colour(embedded_css)

        if not colour:
            css_url = soup.select_one('link[href*=css]')['href']

            contents = Downloader.get(urllib.parse.urljoin(
                url, css_url)).decode('utf-8')

            colour = WebParser.get_background_colour(contents)

        return urllib.parse.urljoin(url, img['src']), colour

    def get_background_colour(css):
        css = css.replace('.title-bar {', '.title-bar{')

        title_bar_indexes = [
            m.start() for m in re.finditer('.title-bar{', css)
        ]

        for title_bar_index in reversed(title_bar_indexes):
            rule = css[title_bar_index:]
            rule = rule[:rule.index('}')]
            rule = rule.replace(' :', ':')

            if 'background-color:' in rule:
                rule = rule[rule.index('background-color:') + 17:]
            elif 'background:' in rule:
                rule = rule[rule.index('background:') + 11:]
            else:
                continue

            if ';' in rule:
                rule = rule[:rule.index(';')]

            return rule.strip()

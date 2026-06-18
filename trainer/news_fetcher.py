"""
Fetches real kids news from:
  - https://newsforkids.net/   (RSS feed)
  - https://www.dogonews.com/  (HTML scrape)
  - https://www.timeforkids.com/ (HTML scrape)

Caches results in Django cache for 6 hours.
Falls back to static NEWS pool on any error.
"""
import xml.etree.ElementTree as ET
import re
import logging
from datetime import date, datetime

logger = logging.getLogger(__name__)

try:
    import requests
    from bs4 import BeautifulSoup
    _DEPS_OK = True
except ImportError:
    _DEPS_OK = False

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
_TIMEOUT = 8

SOURCE_LABELS = {
    'newsforkids': {'label': 'News For Kids', 'url': 'https://newsforkids.net', 'emoji': '📰'},
    'dogonews':    {'label': 'Dogo News',     'url': 'https://www.dogonews.com', 'emoji': '🐾'},
    'timeforkids': {'label': 'Time For Kids', 'url': 'https://www.timeforkids.com', 'emoji': '⏰'},
}


def _clean(text: str) -> str:
    """Strip HTML tags, fix encoding artifacts, collapse whitespace."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('\xa0', ' ').replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('�', '')   # Unicode replacement char (encoding mismatch)
    text = text.replace('â€™', "'").replace('â€œ', '"')
    text = text.replace('–', '-').replace('—', '--')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _fetch_newsforkids(n=5) -> list[dict]:
    """Fetch latest articles from newsforkids.net via RSS + full article body."""
    items = []
    try:
        r = requests.get('https://newsforkids.net/feed/', timeout=_TIMEOUT, headers=_HEADERS)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        rss_items = root.findall('.//item')[:n]

        for rss in rss_items:
            title = _clean(rss.findtext('title', ''))
            link  = _clean(rss.findtext('link', ''))
            desc  = _clean(rss.findtext('description', ''))
            pub   = rss.findtext('pubDate', '')

            body = _fetch_article_body_newsforkids(link) if link else desc
            if not body:
                body = desc

            items.append({
                'id': f'live_nfk_{abs(hash(link)) % 99999}',
                'category': 'news',
                'emoji': '📰',
                'title': title,
                'teaser': desc[:140] + ('…' if len(desc) > 140 else ''),
                'body': body,
                'challenge': 'Share this story with one person today — tell them why it matters in your own words.',
                'tag': 'News For Kids',
                'source_url': link,
                'source_label': 'newsforkids.net',
                'pub_date': pub[:16] if pub else '',
            })
    except Exception as e:
        logger.warning(f'newsforkids fetch failed: {e}')
    return items


def _fetch_article_body_newsforkids(url: str) -> str:
    try:
        r = requests.get(url, timeout=_TIMEOUT, headers=_HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.select_one('.entry-content, .post-content, article .content')
        if not content:
            return ''
        paras = [_clean(p.get_text()) for p in content.find_all('p')
                 if len(p.get_text(strip=True)) > 35]
        return '\n\n'.join(paras[:6])
    except Exception:
        return ''


def _fetch_dogonews(n=5) -> list[dict]:
    """Fetch latest articles from dogonews.com via homepage scrape + article body."""
    items = []
    try:
        r = requests.get('https://www.dogonews.com/', timeout=_TIMEOUT, headers=_HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        seen = set()
        links = []
        for a in soup.select('a[href]'):
            href = a.get('href', '')
            text = a.get_text(strip=True)
            # dogonews article URLs look like /2026/6/5/title-slug
            if re.match(r'^/\d{4}/\d+/\d+/.+', href) and href not in seen and len(text) > 10:
                seen.add(href)
                links.append(('https://www.dogonews.com' + href, text))
                if len(links) >= n:
                    break

        for url, title in links:
            body, teaser = _fetch_article_body_dogonews(url)
            items.append({
                'id': f'live_dogo_{abs(hash(url)) % 99999}',
                'category': 'news',
                'emoji': '🐾',
                'title': title,
                'teaser': teaser[:140] + ('…' if len(teaser) > 140 else ''),
                'body': body or teaser,
                'challenge': 'After reading, write three bullet points summarising: what happened, why it matters, and what comes next.',
                'tag': 'Dogo News',
                'source_url': url,
                'source_label': 'dogonews.com',
                'pub_date': '',
            })
    except Exception as e:
        logger.warning(f'dogonews fetch failed: {e}')
    return items


def _fetch_article_body_dogonews(url: str) -> tuple[str, str]:
    try:
        r = requests.get(url, timeout=_TIMEOUT, headers=_HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.select_one('.article-body, .post-content, .entry-content')
        if not content:
            return '', ''
        paras = [_clean(p.get_text()) for p in content.find_all('p')
                 if len(p.get_text(strip=True)) > 35]
        full = '\n\n'.join(paras[:6])
        teaser = paras[0] if paras else ''
        return full, teaser
    except Exception:
        return '', ''


_TFK_TOPIC_PAGES = [
    'https://www.timeforkids.com/g2/topics/animals/',
    'https://www.timeforkids.com/g2/topics/science/',
    'https://www.timeforkids.com/g2/topics/environment/',
    'https://www.timeforkids.com/g2/topics/inventions/',
    'https://www.timeforkids.com/g2/topics/people/',
]


def _fetch_timeforkids(n=4) -> list[dict]:
    """Fetch latest articles from timeforkids.com topic pages."""
    items = []
    seen_urls = set()
    try:
        for topic_url in _TFK_TOPIC_PAGES:
            if len(items) >= n:
                break
            try:
                r = requests.get(topic_url, timeout=_TIMEOUT, headers=_HEADERS)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.select('a[href]'):
                    href = a.get('href', '')
                    text = a.get_text(strip=True)
                    if (re.search(r'timeforkids\.com/g\d+/[a-z]', href) and
                            '-g' in href and href not in seen_urls and
                            len(text) > 5 and 'Articles' not in text):
                        seen_urls.add(href)
                        body, teaser = _fetch_article_body_tfk(href)
                        if not body:
                            continue
                        items.append({
                            'id': f'live_tfk_{abs(hash(href)) % 99999}',
                            'category': 'news',
                            'emoji': '⏰',
                            'title': text,
                            'teaser': teaser[:140] + ('…' if len(teaser) > 140 else ''),
                            'body': body,
                            'challenge': 'Find one extra fact about this topic and share it with someone.',
                            'tag': 'Time For Kids',
                            'source_url': href,
                            'source_label': 'timeforkids.com',
                            'pub_date': '',
                        })
                        if len(items) >= n:
                            break
            except Exception:
                continue
    except Exception as e:
        logger.warning(f'timeforkids fetch failed: {e}')
    return items


def _fetch_article_body_tfk(url: str) -> tuple[str, str]:
    try:
        r = requests.get(url, timeout=_TIMEOUT, headers=_HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.select_one('main')
        if not content:
            return '', ''
        paras = [_clean(p.get_text()) for p in content.find_all('p')
                 if len(p.get_text(strip=True)) > 35]
        full = '\n\n'.join(paras[:5])
        teaser = paras[0] if paras else ''
        return full, teaser
    except Exception:
        return '', ''


def fetch_all_live_news(max_total=12) -> list[dict]:
    """
    Fetch live news from all three sources, interleaved by source.
    Returns up to max_total articles.
    """
    if not _DEPS_OK:
        return []

    nfk  = _fetch_newsforkids(n=5)
    dogo = _fetch_dogonews(n=5)
    tfk  = _fetch_timeforkids(n=4)

    # Interleave: one from each source in rotation
    combined = []
    for a, b, c in zip(nfk, dogo, tfk):
        combined.extend([a, b, c])
    # Append remainders
    for extra in (nfk[3:] + dogo[3:] + tfk[3:]):
        combined.append(extra)

    return combined[:max_total]


def get_live_news_cached(django_cache) -> list[dict]:
    """
    Return live news, using Django cache (6-hour TTL).
    Returns [] on failure so caller can fall back to static pool.
    """
    cache_key = f'live_news_{date.today()}'
    cached = django_cache.get(cache_key)
    if cached is not None:
        return cached

    articles = fetch_all_live_news()
    if articles:
        django_cache.set(cache_key, articles, 60 * 60 * 6)
    return articles


def pick_news_item(articles: list[dict], seen_ids: list) -> dict | None:
    """Pick today's article avoiding already-seen ones."""
    if not articles:
        return None
    unseen = [a for a in articles if a['id'] not in seen_ids]
    pool = unseen if unseen else articles
    # rotate by day-of-year so different article each day
    idx = date.today().timetuple().tm_yday % len(pool)
    return pool[idx]

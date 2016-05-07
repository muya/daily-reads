from newspaper import Article


def extract_url(tweet):
    url_entities = tweet['entities']['urls']
    for url in url_entities:
        if 'expanded_url' in url:
            return url['expanded_url']

    return None


def extract_article(url):
    article = Article(url)
    print('About to parse & download article: %s...' % url)
    article.download()
    print('Download complete!')
    article.parse()
    print('Parse complete!')

    article_data = {}
    article_data['title'] = article.title
    article_data['img'] = article.top_image
    article_data['publish_date'] = article.publish_date
    if article.text:
        # first paragraph
        article_text = article.text.split('\n\n')[0]
    else:
        article_text = ''

    article_data['text'] = article_text.encode('ascii', 'ignore')

    print('Article data obtained: %s' % article_data)
    return article_data

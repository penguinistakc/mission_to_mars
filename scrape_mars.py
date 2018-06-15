from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from collections import OrderedDict


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def mars_news():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news'  
    browser.visit(news_url)
#    html = browser.html
#    soup = bs(html, 'html.parser')
#    something=soup.select_one("div.content_title").find("a")
#    print(something)
    browser.find_by_name('content_title')
    browser.click_link_by_partial_href('news/')
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.select_one('h1.article_title').text
    news_p = soup.select_one('div.wysiwyg_content').text
    return news_title, news_p


def mars_space_image():
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov'
    space_images_url = '/spaceimages'
    search_url = '/?search=&category=Mars'
    jpl_mars_space_image_url = jpl_url + space_images_url + search_url
    browser.visit(jpl_mars_space_image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    jpl_image = image_soup.footer.a['data-fancybox-href']
    return jpl_url + jpl_image


def mars_weather_tweet():
    browser = init_browser()
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    tweet_html = browser.html
    tweet_soup = bs(tweet_html, 'html.parser')
    return tweet_soup.find('p', class_="TweetTextSize").next_element


def mars_facts():
    facts_url = 'http://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    facts_ds = tables[0]
    facts_ds.columns = ['Category', 'Fact']
    facts_ds.set_index('Category', inplace=True)
    html_string = facts_ds.to_html()
    return html_string.replace('\n', '')


def mars_hemisphere_images():
    browser = init_browser()
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hem_images = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced',
                  'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
    hemisphere_image_urls = []
    for image in hem_images:
        hem_image_data = {}
        browser.visit(hem_url)
        browser.click_link_by_partial_text(image)
        page_title = browser.title
        mhi_html = browser.html
        mhi_soup = bs(mhi_html, 'html.parser')
        page_url = mhi_soup.select_one("div.downloads").ul.li.a['href']
        hem_image_data = {
            'title': page_title,
            'img_url': page_url
        }
        hemisphere_image_urls.append(hem_image_data)
    return hemisphere_image_urls


def scrape():
    news_title, news_p = mars_news()
    return {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': mars_space_image(),
        'mars_weather': mars_weather_tweet(),
        'mars_facts': mars_facts(),
        'hemisphere_image_urls': mars_hemisphere_images()
    }


if __name__ == '__main__':
    scrape()

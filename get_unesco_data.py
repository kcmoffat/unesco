from urllib2 import urlopen
import lxml
import re
from bs4 import BeautifulSoup
from MySQLdb import connect

def get_name(soup):
    try:
        name = unicode(soup.title.string)
        return name
    except AttributeError:
        return None

def get_country(soup):
    try:
        country = unicode(soup(href=re.compile("statesparties"))[0].string)
        return country
    except IndexError:
        return None

def get_image_url(soup):
    try:
        image_url = u"http://whc.unesco.org" + unicode(soup('div', class_="icaption")[0].contents[1].contents[0]['src'])
        return image_url
    except IndexError:
        return None

def get_brief_desc(soup):
    try:
        brief_desc = unicode(soup(id="des_default")[0].contents[1])
        return brief_desc
    except IndexError:
        return None

def get_long_desc(soup):
    try:
        next = soup('h4', text="Long Description")[0].find_next_sibling("p")
        result = unicode(next)
        while next.name != 'small':
            next = next.find_next_sibling()
            result = result + unicode(next)
        return result
    except IndexError:
        return None

def get_is_404(name):
    if name == None:
        return True
    else:
        return False

def get_is_complete(name, country, image_url, brief_desc, long_desc):
    if name != None and country != None and image_url != None and brief_desc != None and long_desc != None:
        return True
    else:
        return False

def get_unesco_data(min_id=1, max_id=1):
    result = []
    for unesco_id in range(min_id, max_id + 1):        

        response = urlopen("http://whc.unesco.org/en/list/" + str(unesco_id))
        page = response.read()
        soup = BeautifulSoup(page, "lxml")

        name = get_name(soup)
        country = get_country(soup)
        image_url = get_image_url(soup)
        brief_desc = get_brief_desc(soup)
        long_desc = get_long_desc(soup)
        is_404 = get_is_404(name)
        is_complete = get_is_complete(name, country, image_url, brief_desc, long_desc)

        result.append([unesco_id, name, country, image_url, brief_desc, long_desc, is_404, is_complete])
    return result

#unesco_data = get_unesco_data(51, 1500)

# Store the retrieved data in a MySQL db on localhost
db = connect(host = "localhost", user = "root", passwd = "test123", db = "site_data", charset='utf8')
c = db.cursor()
c.executemany(
    """INSERT INTO test4 (unesco_id, name, country, image_url, brief_desc, long_desc, is_404, is_complete)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
    unesco_data
    )

c.close()
db.commit()
db.close()

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError


"""
Returns the title object of the html page as a Tag object.
If page or server is not found or cannot be connected to, returns None

Parameter url: the url address of the page
Precondition: url is a str
"""
def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    
    try:
        bsObj = BeautifulSoup(html.read(), "lxml")
        title = bsObj.body.h1
    except AttributeError:
        return None
    return title

"""
Returns NavigableString object list of all children of the first tag passed
with the passed attributes for the webpage given by the passed url. If page
or server is not found or cannot be connected to, returns None.

Parameter url: the url address of the page
Precondition: url is a str

Parameter tag: the html element to find children of
Precondition: tag is a str

Parameter attributes: the attributes that the tag should have
Preconditon: attributes is a dictionary
"""
def getChildren(url, tag, attributes=''):
    try:
        html = urlopen(url)
    except HTTPError:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "lxml")
        children = bsObj.find(tag, attributes).children
    except AttributeError:
        return None
    return children

"""
Returns all the links to other pages located on a static page.

Parameter url: the url address of the page
Precondition: url is a str
"""
def getLinks(url):
    import re
    
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a"):
        if 'href' in link.attrs:
            print(link.attrs['href'])

"""
Returns the first page element that matchs the specified page element tag and attributes.

Parameter url: a valid webapge url
Precondition: url is a string

Parameter tag: an element tag on the page
Precondition: tag is a string

Parameter attrs: the specified attribute
Precondition: attrs is a string or dict
"""
def getPageElement(url, tag, attrs = ""):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        bsObj = BeautifulSoup(html, 'lxml')
        item = bsObj.find(tag, attrs)
        try:
            return item
        except AttributeError:
            print('Attribute error. Are the attributes of that tag valid?')
    except HTTPError:
        print('Http error')
        
    except ValueError:
        print('Value error. Is the url valid?')
"""
Returns  all of the page elements that match specified page element tag and attributes.
This function is able to by-pass the server security feature of some sites that block known
spider/bot user agents.

Parameter url: a valid webapge url
Precondition: url is a string

Parameter tag: an element tag on the page
Precondition: tag is a string

Parameter attrs: the specified attribute
Precondition: attrs is a string or dict
"""
def getPageElements(url, tag, attrs = ""):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        bsObj = BeautifulSoup(html, 'lxml')
        items = bsObj.findAll(tag, attrs)
        try:
            return items
        except AttributeError:
            print('Attribute error. Are the attributes of that tag valid?')
    except HTTPError:
        print('Http error')
        
    except ValueError:
        print('Value error. Is the url valid?')
  
"""
Removes html tags from a string
Parameter text: the string to remove HMTL tags from
Precondition: text is a string
"""
def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

"""
Creates a pop-up message
"""
def popupmsg(msg, title, buttonmsg):
    import easygui
    try:
        easygui.msgbox(msg, title, ok_button=str(buttonmsg))
    except:
        print('error in creating pop-up. Are you passing in strings?')

    

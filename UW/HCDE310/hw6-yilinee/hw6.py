import urllib.request, urllib.error, urllib.parse, json, webbrowser
import flickr_key

### Utility functions you may want to use

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request." )
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

#### Main Assignment ##############
#import flickr_key as flickr_key
def flickrREST(baseurl = 'https://api.flickr.com/services/rest/',
    method = 'flickr.photos.search',
    api_key = flickr_key.key,
    format = 'json',
    params={},
    printurl = False
    ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"]=True
    url = baseurl + "?" + urllib.parse.urlencode(params)
    if printurl:
        print(url)
    return safe_get(url)

#######################
## Building block 1 ###
# Define a function called get_photo_ids() which uses the Flickr API 
# to search for photos with a given tag, and return a list of photo 
# IDs for the corresponding photos. 
#
# * Use a list comprehension to generate the list. *
#
# Inputs:
#   tag: a tag to search for
#   n: the number of search results per page
#      (default value should be 100)
#
# Returns: a list of (at most) n photo ids, or None if an
#          error occurred

def get_photo_ids(tag, n = 100):
    value = flickrREST(params={"tags":tag, "per_page":n})
    str = value.read()
    d = json.loads(str)
    if value is not None:
        ids = [item["id"] for item in d["photos"]["photo"]]
        return ids
    return None

######################
## Building block 2 ##
#
# Define a function called get_photo_info() which uses the Flickr API
# to get information about a particular photo id. The information
# should be returned as a dictionary Hint: use flickrREST and the 
# Flickr API method flickr.photos.getInfo, documented at
# http://www.flickr.com/services/api/flickr.photos.getInfo.html
#
# Inputs:
#   photoid: the id of the photo to get information about
#
# Returns: a dictionary with information about that photo,
#          or None if an error occurred.

def get_photo_info(photoid):
    value = flickrREST(method="flickr.photos.getInfo", params={"photo_id": photoid})
    str = value.read()
    d = json.loads(str)
    if value is not None:
        return d
    return None

######################
## Building block 3 ##
#
# Define a class called Photo to represent Flickr photos
#
# It should have three methods:
# (a) a constructor (__init__())
# (b) make_photo_url(), which returns URLs to access photos
# (c) a string representation (__str__())
#
# Details for those methods are below.

class Photo():
    """A class to represent a photo from Flickr"""
## (a) __init__():
# The constructor (recall that the __init__() method is called the 
# constructor) should take a dictionary representing photo info as a
# paramter and initialize eight instance variables:
#  -title: the title of the photo (Use "_content"!)
#  -author: the user that posted the photo (use username!)
#  -userid: the user nsid (####@N##, for example)
#  -tags: a list of tags (strings) associated with the photo
#         (Use "_content"!)
#         * Your constructor should use a list comprehension to 
#         create the tags list.*    
#  -comment_count: a count with the number of comments on the photo
#  -num_views: the number of times the photo was viewed
#  -url: the location of the photo page on Flickr
#  -farm: the server farm on which this image exists
#  -server: the server on which this image exists
#  -id: the photo id (use "id")
#  -secret: the "secret" for the photo.
#
    def __init__(self, d):
        """Initialize the Photo class"""
        self.title = d['photo']['title']['_content']
        self.author = d['photo']['owner']['username']
        self.userid = d['photo']['owner']['nsid']
        self.tags = [item['_content'] for item in d['photo']['tags']['tag']]
        self.comment_count = int(d['photo']['comments']['_content'])
        self.num_views = int(d['photo']['views'])
        self.url = d['photo']['urls']['url'][0]['_content']
        self.farm = int(d['photo']['farm'])
        self.server = d['photo']['server']
        self.id = d['photo']['id']
        self.secret = d['photo']['secret']

## (b) make_photo_url()
# Next, define a method that returns the URL a photo image.
# Call this method make_photo_url.
# It should take one parameter:
# - size: The size of the photo. This should be one of the sizes 
#         in https://www.flickr.com/services/api/misc.urls.html
#         e.g., "q" for a 150x150px square.
#         This should default to "q"!
#
# The above method also describes how to make photo URLs based on the
# information in the photo dictionary.
#
# This method should return the URL.
#
    def make_photo_url(self, size='q'):
        return 'https://live.staticflickr.com/' + self.server + '/' + self.id + '_' + self.secret + '_' + size + '.jpg'

## (c) __str__()
# The __str__() method should return a string with the
# following format and information:
#   ~~~ {{photo title}} ~~~
#   author: {{author}}
#   number of tags: {{number of tags}}
#   views: {{number of views}}
#   comments: {{number of comments}}
#   url: {{url to the photo page}}
#
    def __str__(self):
        return '~~~ ' + self.title + ' ~~~\n' + 'author: ' + self.author + '\nnumber of tags: ' + str(len(self.tags)) \
               + '\nviews: ' + str(self.num_views) + '\ncomments: ' + str(self.comment_count) + '\nurl: ' + self.url

if __name__ == '__main__':
    ### Testing your building blocks
    print('\n\nTesting your building blocks\n------------')
    #
    # Test get_photo_ids() with the following line of code, which
    # will give four photo IDs that match the query "hamster".
    #
    # The ids you get may be different than what's in the sample 
    # output - you are working with live data!
    #
    print(get_photo_ids('hamster', n=4))

    # Test get_photo_info() with the following two lines of code:
    
    pd = get_photo_info(5140736446)
    print(pd)

    # Test your Photo class with the following lines of code.
    # Check the format of your output against sample output in the 
    # README file, and make adjustments to your __init__ and __str__ 
    # methods as needed.
    
    po = Photo(pd)
    print(po)
    print(po.tags)
    webbrowser.open(po.url)
    
##############
### Part 1 ###
# Use your get_photo_ids function to get a list of 100 photo ids
# with a tag of your choosing.
#
# Convert the list of ids into a list of Photo objects using a
# list comprehension. You will need the get_photo_info() function
# to do this.

ilist = get_photo_ids("husky", n = 100)
plist = [get_photo_info(item) for item in ilist]

##############
### Part 2 ###
# (a) Order the photo objects by number of views.
#     Print the five most viewed photos.

print("\nTop Five Photos by Views")
print("------------")

vplist = sorted(plist, key = lambda i: Photo(i).num_views, reverse=True)
for d in vplist[0:5]:
    print(Photo(d))

# (b) Order the photo objects by number of tags.
#     Print the five most tagged photos
print("\nTop Five Photos by Number of Tags")
print("------------")

tplist = sorted(plist, key = lambda i: len(Photo(i).tags), reverse=True)
for d in tplist[0:5]:
    print(Photo(d))

# (c) Order the photo objects by number of comments.
# Print the five most commented photos

print("\nTop Five Photos by Number of Comments")
print("------------")

cplist = sorted(plist, key = lambda i: Photo(i).comment_count, reverse=True)
for d in cplist[0:5]:
    print(Photo(d))

##############
### Part 3 ###
# Compute the total number of views received by each author in
# the photo object list.
#
# Then, print out the username of the author along with the total
# number of views their photos had received, for the top ten
# users, ranked in order of number of views, in the following
# format:
# (1) Meena: 1221
# (2) Akeiylah: 134
# (3) Yihan: 120
# (4) Jeremy: 113
# (5) Saksham: 108
# (6) Nadir: 104
# (7) Valerie: 98
# (8) Varun: 54
# (9) Ben: 12
# (10) Sean: 1
#
# Important: There is a chance that, even with 100 photos, you
# may have less than 10 authors!

print("\nTop ten authors by number of views")
print("------------")

def checkName(d, name):
    if name not in d:
        d[name] = 0

cc = {}

for d in plist:
    dic = Photo(d)
    checkName(cc, dic.author)
    cc[dic.author] += dic.num_views

csort = dict(sorted(cc.items(), key=lambda i: i[1], reverse=True))
csort = csort

count = 0
for k in list(csort.keys())[:10]:
    count += 1
    result = '(' + str(count) + ') ' + k + ': ' + str(csort[k])
    print(result)

###############
###  Part 4 ###
# Output an HTML page with the top five images for views, tags,
# and comments (from part 2).
#
# You may style your page as much as you like, but this is optional.
#
# Fill in your code here

##################
### Finally... ###
# Based on the photos you get, which do you think is a better way
# to find good photos, the ones with the most views, most
# comments, or the most tags?
print("------------")
print("""your thoughts here""")
print("I think the ones with most comments would serve well in this case. The number of comments is the least "
      "subjective factor, compared to the number of view sor tags, to evaluate a photo's quality.")

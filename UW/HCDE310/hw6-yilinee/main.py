from hw6 import vplist, tplist, cplist
from hw6 import Photo
from flask import Flask, render_template

def checkName(d, name):
    if name not in d:
        d[name] = ""

dlist = []
for it in vplist[0:5]:
    titled = Photo(it).title
    urld = Photo(it).make_photo_url()
    templist = [urld, titled]
    dlist.append(templist)
for it in tplist[0:5]:
    titled = Photo(it).title
    urld = Photo(it).make_photo_url()
    templist = [urld, titled]
    dlist.append(templist)
for it in cplist[0:5]:
    titled = Photo(it).title
    urld = Photo(it).make_photo_url()
    templist = [urld, titled]
    dlist.append(templist)

app = Flask(__name__)

@app.route("/")

def hello():
    """ Return a greeting """
    title = "Results of Husky"
    data = dlist
    return render_template('index.html',title=title,data=data)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)



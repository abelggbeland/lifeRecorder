from flask import Flask, request, jsonify, abort
import json
import os
import hashlib
import re

app = Flask(__name__)

key = "1394e8e473378f583f0a85462254b6fb"

# result = hashlib.md5(b'EVwRqCL6ss6wBGrgXPJBkMz')

print()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/setdata', methods=['POST'])
def set_data():
    data = request.json
    if key == data["key"]:
        dateraw = data["date"]
        date = str(dateraw).split(" ")
        formatedDate = date[0] + "-" + date[1][:2] + "-" + date[2]
        shortdate = date[0] + "-" + date[1][:2] + "-" + date[4][:1] + "-" + date[4][2:4] + "-" + date[5]
        if not os.path.isdir("json/" + formatedDate):
            os.makedirs("json/" + formatedDate)

        with open("json/" + formatedDate + f"/{shortdate}{'-' + data['type'] if data['type'] != 'hour' else ''}.json", "w") as f:
            json.dump(data, f)
        return jsonify(request.json)
    else:
        return abort(403)

@app.route('/getdata/<date>/<keysend>', methods=['GET'])
def get_data(date=None, keysend=None):
    if key != keysend:
        return abort(403)

    dateedit = str(date).split("-")
    print(dateedit)

    if re.match("^[a-zA-Z]+\-+[0-9]+\-+[0-9]{4}$", date) != None:
        if not os.path.isdir("json/" + date):
            return "abort(404) - 1"
        else:
            files = os.listdir("json/" + date)
            print(files)
            datajsonlist = {}
            for i in range(len(files)):
                with open("json/" + date + "/" + files[i]) as filer:
                    datajsonlist[files[i]] = json.load(filer)
            return jsonify(datajsonlist)

    elif re.match("^[a-zA-Z]+\-+[0-9]+\-+[0-9]+\-+[0-9]+\-+[0-9]+\-+[a-zA-Z]+[a-zA-Z\-]+$", date) != None:
        if not os.path.isdir("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2]):
            return "abort(404) - 2"
        else:
            print("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                              dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                              dateedit[5] + ".json")
            if os.path.isfile("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                              dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                              dateedit[5] + ".json"):
                with open("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                              dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                              dateedit[5] + ".json") as f:
                    return json.load(f)
            elif os.path.isfile("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                              dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                              dateedit[5] + "-" + "morning.json"):
                with open("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                          dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                          dateedit[5] + "-" + "morning.json") as f:
                    return json.load(f)
            elif os.path.isfile("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                              dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                              dateedit[5] + "-" + "night.json"):
                with open("json/" + dateedit[0] + "-" + dateedit[1] + "-" + dateedit[2] + "/" +
                          dateedit[0] + "-" + dateedit[1] + "-" + dateedit[3] + "-" + dateedit[4] + "-" +
                          dateedit[5] + "-" + "night.json") as f:
                    return json.load(f)
            else:
                return abort(404)
    else:
        return abort(404) - 4


if __name__ == '__main__':
    app.run()

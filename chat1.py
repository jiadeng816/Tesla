from flask import Flask,render_template,request as req,redirect,url_for
import json
import urllib
import urllib.request

app = Flask(__name__)

@app.route("/")
def show():
    return render_template("communication1.html")

@app.route('/chat', methods=['GET', 'POST'])
def index():
    if req.method == 'POST':
        global data
        data = req.form.get("chat")
        print(data)
    headers = {'Content-Type': 'application/json'}
    access_token = '24.b9b7753e9bea4da949e3d6ce30a80f3d.2592000.1567755786.282335-16968761'
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token
    post_data = "{\"log_id\":\"UNITTEST_10000\",\"version\":\"2.0\",\"service_id\":\"S18902\",\"session_id\":\"\",\"request\":{\"query\":\""+data+"\",\"user_id\":\"88888\"},\"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"60877\"]}}}"
    print(post_data)
    request = urllib.request.Request(url, data=post_data.encode('utf-8'), headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")
    if content:
        a = json.loads(content)
        b = a["result"]["response_list"][0]["action_list"][0]["say"]
    context={
        'response':b,
    }
    return json.dumps(context)

if __name__ == '__main__':
    app.run(debug=True)
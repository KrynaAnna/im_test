from flask import Flask, request, render_template
from test3 import main

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        lat = float(request.form.get('lat'))
        lng = float(request.form.get('lng'))
        main(url=url, destination_=f'{lat},{lng}')
        result_text = "Success! You can check your google sheet with updated data!"
        return render_template('home.html', lat=lat, lng=lng, url=url, result=result_text)
    return render_template('home.html', lat='', lng='', url='https://docs.google.com/spreadsheets/d/1cQvWXRn_vaJQxEolBvlBKDPQCuKEYnq65NGiyx7Y04k/edit#gid=0', result='')


if __name__ == '__main__':
    app.run(debug=True)

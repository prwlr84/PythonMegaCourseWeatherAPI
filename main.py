from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('page.html')


@app.route('/api/v1/<station>/<date>')
def api(station, date):
    temperature = 23
    df = pd.read_csv()
    return {'date': date,
            'station': station,
            'temperature': temperature}


if __name__ == '__main__':
    app.run(debug=True)

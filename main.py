from time import strftime

from flask import Flask, render_template
import pandas as pd
import zipfile
from io import StringIO  # Import StringIO


def get_txt(station_id=None):
    if station_id:
        file_to_read = f'TG_STAID{str(station_id).zfill(6)}.txt'
    else:
        file_to_read = 'stations.txt'

    with zipfile.ZipFile('data-small.zip', 'r') as zip_ref:
        with zip_ref.open(file_to_read) as file:
            return file.read().decode('utf-8')


def format_date(string):
    return f"{string[:4]}-{string[4:6]}-{string[6:]}"


def get_df(station, parse_date=True):
    data = StringIO(get_txt(station))
    return pd.read_csv(data, skiprows=20, parse_dates=['    DATE'] if parse_date else None)


app = Flask(__name__)
stations = pd.read_csv(StringIO(get_txt()), skiprows=17)


@app.route('/')
def home():
    return render_template('page.html', data=stations.to_html())


@app.route('/api/v1/<station>/yearly/<year>')
def api1(station, year):
    df = get_df(station, parse_date=False)
    df['    DATE'] = df['    DATE'].astype(str)
    return df[df['    DATE'].str.startswith(str(year))]


@app.route('/api/v1/<station>/<date>')
def api2(station, date):
    df = get_df(station)
    temperature = df.loc[df['    DATE'] == format_date(date)]['   TG'].squeeze() / 10
    return {'date': format_date(date),
            'station': station,
            'temperature': temperature}


@app.route('/api/v1/<station>')
def api3(station):
    return get_df(station).to_dict(orient='records')


if __name__ == '__main__':
    app.run(debug=True, port=5001)

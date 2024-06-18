from flask import Flask, jsonify, render_template
import csv
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s')
speed_log = 'speed.log'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/data')
def data():
    data_points = []
    with open(speed_log, 'r') as file:
        reader = csv.DictReader(file, delimiter=' ')
        for row in reader:
            data_points.append({
                'date': f"{row['Date']} {row['Time']}",
                'speed': float(row['DownloadSpeed'])
            })
    return jsonify(data_points)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Menambahkan CORS di seluruh aplikasi

# Fungsi untuk scraping data harga emas
def get_gold_prices():
    url = 'https://harga-emas.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tanggal = soup.select('tr.title_table:nth-child(1) td')[0].text.strip()
    judul_kolom = [td.text.strip() for td in soup.select('tr.title_table:nth-child(2) td')]
    harga = [td.text.strip() for td in soup.select('tr:nth-child(4) td')]
    waktu = [td.text.strip() for td in soup.select('tr:nth-child(5) td')]

    return {
        'tanggal': tanggal,
        'judul_kolom': judul_kolom,
        'harga': harga,
        'waktu': waktu
    }

@app.route('/api/gold_prices', methods=['GET'])
def api_gold_prices():
    gold_data = get_gold_prices()
    return jsonify(gold_data)

if __name__ == '__main__':
    app.run(debug=True)

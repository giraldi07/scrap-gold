from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS  # Impor CORS

app = Flask(__name__)

# Terapkan CORS pada aplikasi Flask
CORS(app)  # Secara default mengizinkan semua domain

# Fungsi untuk scraping data harga emas
def get_gold_prices():
    url = 'https://harga-emas.org/'  # Ganti dengan URL yang sesuai untuk scraping
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Mengambil data berdasarkan selector yang sudah dijelaskan
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
def gold_prices_api():
    # Mengambil data harga emas
    gold_data = get_gold_prices()

    # Mengambil data harga emas dari tabel 2
    url = 'https://harga-emas.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table2_data = []
    table2 = soup.find_all('table', {'class': 'in_table'})
    
    if len(table2) > 1:
        table2 = table2[1]  # Mengambil tabel kedua
        rows = table2.find_all('tr')

        # Mengambil data Spot Harga Emas Hari Ini dan Konversi Satuan
        for row in rows[2:6]:
            columns = row.find_all('td')
            if len(columns) == 7:  # Pastikan ada 7 kolom
                table2_data.append([col.get_text(strip=True) for col in columns])

    table3_data = []
    if len(table2) > 2:
        table3 = soup.find_all('table', {'class': 'in_table'})[2]  # Mengambil tabel ketiga
        rows = table3.find_all('tr')

        # Mengambil data harga Emas per Gram dan per Batangan
        for row in rows[2:]:
            columns = row.find_all('td')
            if len(columns) == 5:  # Pastikan ada 5 kolom
                table3_data.append([col.get_text(strip=True) for col in columns])

    # Membuat response API dalam format JSON
    return jsonify({
        'gold_data': gold_data,
        'table2_data': table2_data,
        'table3_data': table3_data
    })

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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



@app.route('/')
def index():
    # Melakukan scraping data
    url = 'https://harga-emas.org/'
    response = requests.get(url)

    # Pastikan respons berhasil
    if response.status_code != 200:
        return f"Error: Gagal mengambil halaman, status code: {response.status_code}"

    soup = BeautifulSoup(response.content, 'html.parser')


    # Table 2: Spot Harga Emas Hari Ini (Market Open) and Konversi
    table2_data = []
    table2 = soup.find_all('table', {'class': 'in_table'})
    
    # Debugging: Pastikan tabel ditemukan
    print(f"Total tables found: {len(table2)}")
    
    if len(table2) > 1:
        table2 = table2[1]  # Mengambil tabel kedua
        rows = table2.find_all('tr')

        # Mengambil data Spot Harga Emas Hari Ini dan Konversi Satuan
        for row in rows[2:6]:  # Baris untuk Spot Harga Emas
            columns = row.find_all('td')
            if len(columns) == 7:  # Pastikan ada 7 kolom
                table2_data.append([col.get_text(strip=True) for col in columns])

    # Debug: Cek data Table 2
    print(f"Table 2 Data: {table2_data}")

    # Table 3: Harga Emas (Gram dan Batangan)
    table3_data = []
    if len(table2) > 2:
        table3 = soup.find_all('table', {'class': 'in_table'})[2]  # Mengambil tabel ketiga
        rows = table3.find_all('tr')

        # Mengambil data harga Emas per Gram dan per Batangan untuk Gedung Antam dan Pegadaian
        for row in rows[2:]:  # Mengambil semua baris setelah header
            columns = row.find_all('td')
            if len(columns) == 5:  # Pastikan ada 5 kolom
                table3_data.append([col.get_text(strip=True) for col in columns])

    # Debug: Cek data Table 3
    print(f"Table 3 Data: {table3_data}")




    # Render template with all table data
    gold_data = get_gold_prices()
    return render_template('index.html', 
                           gold_data=gold_data, 
                           table2_data=table2_data,
                           table3_data=table3_data,
                           )


if __name__ == '__main__':
    app.run(debug=True)

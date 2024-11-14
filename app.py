from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    # Melakukan scraping data
    url = 'https://harga-emas.org/'
    response = requests.get(url)

    # Pastikan respons berhasil
    if response.status_code != 200:
        return f"Error: Gagal mengambil halaman, status code: {response.status_code}"

    soup = BeautifulSoup(response.content, 'html.parser')

    # Mencetak HTML lengkap untuk melihat struktur
    # print(soup.prettify())

    # Debugging: cek keseluruhan HTML
    # print(soup.prettify())

    # Mengambil tanggal dengan pengecekan jika elemen ada
    date_element = soup.find("div", {"class": "date"})
    if date_element:
        date = date_element.get_text(strip=True)
    else:
        date = "Tanggal tidak ditemukan"
    
    # Debugging: Pastikan elemen ditemukan
    print(f"Date: {date}")

    # Mengambil data Spot Harga Emas per Ounce dan per Gram
    usd_spot_per_ounce = soup.find("span", {"class": "usd_spot_ounce"})
    if usd_spot_per_ounce:
        usd_spot_per_ounce = usd_spot_per_ounce.get_text(strip=True)
    else:
        usd_spot_per_ounce = "Data tidak ditemukan"
    
    print(f"USD Spot per Ounce: {usd_spot_per_ounce}")

    usd_spot_change = soup.find("span", {"class": "usd_spot_change"})
    if usd_spot_change:
        usd_spot_change = usd_spot_change.get_text(strip=True)
    else:
        usd_spot_change = "Data tidak ditemukan"
    
    print(f"USD Spot Change: {usd_spot_change}")

    usd_spot_per_gram = soup.find("span", {"class": "usd_spot_gram"})
    if usd_spot_per_gram:
        usd_spot_per_gram = usd_spot_per_gram.get_text(strip=True)
    else:
        usd_spot_per_gram = "Data tidak ditemukan"
    
    print(f"USD Spot per Gram: {usd_spot_per_gram}")

    usd_gram_change = soup.find("span", {"class": "usd_gram_change"})
    if usd_gram_change:
        usd_gram_change = usd_gram_change.get_text(strip=True)
    else:
        usd_gram_change = "Data tidak ditemukan"
    
    print(f"USD Gram Change: {usd_gram_change}")

    # Mengambil nilai IDR/USD dan harga spot dunia
    idr_to_usd = soup.find("span", {"class": "idr_to_usd"})
    if idr_to_usd:
        idr_to_usd = idr_to_usd.get_text(strip=True)
    else:
        idr_to_usd = "Data tidak ditemukan"
    
    print(f"IDR to USD: {idr_to_usd}")

    # Simpan data dalam dictionary
    # Table 1 Data: Mengambil data harga emas
    # Menyimpan data yang ditemukan
    table1_data = {
        'Date': date,
    }

    # Mencari elemen yang mengandung "Harga Emas Hari Ini"
    date_element = soup.find("td", string=lambda x: x and "Harga Emas Hari Ini" in x)
    if date_element:
        date = date_element.get_text(strip=True).replace("Harga Emas Hari Ini -", "").strip()
    else:
        date = "Tanggal tidak ditemukan"


    print(f"Date: {date}")



    # Mengambil data USD Spot per Ounce
    usd_spot_ounce_element = soup.find("td", text="USD Spot per Ounce")  # Coba mencari kolom yang sesuai
    if usd_spot_ounce_element:
        usd_spot_ounce = usd_spot_ounce_element.find_next("td").get_text(strip=True)
        table1_data['usd_spot_ounce'] = usd_spot_ounce
    else:
        table1_data['usd_spot_ounce'] = "Data tidak ditemukan"

    # Mengambil perubahan USD Spot
    usd_spot_change_element = soup.find("td", text="Change")
    if usd_spot_change_element:
        usd_spot_change = usd_spot_change_element.find_next("td").get_text(strip=True)
        table1_data['usd_spot_change'] = usd_spot_change
    else:
        table1_data['usd_spot_change'] = "Data tidak ditemukan"

    # Debug: Pastikan data berhasil diambil
    print(f"Table 1 Data: {table1_data}")




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

    # Scraping Table 4 - Additional data structure
    # Tabel 4 - Harga Jual dan Beli
    table4_data = {}
    sell_element = soup.select_one(".halfwidth:nth-child(1) p")
    buy_element = soup.select_one(".halfwidth:nth-child(2) p")

    table4_data['sell_price'] = sell_element.get_text(strip=True) if sell_element else "Data tidak ditemukan"
    table4_data['buy_price'] = buy_element.get_text(strip=True) if buy_element else "Data tidak ditemukan"


    # Render template with all table data
    return render_template('index.html', 
                           table1_data=table1_data, 
                           table2_data=table2_data,
                           table3_data=table3_data,
                           table4_data=table4_data,
                           )


if __name__ == '__main__':
    app.run(debug=True)

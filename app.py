from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi untuk memfilter konfigurasi berdasarkan set ip atau set role
def filter_used_config(config):
    import re
    # Pattern untuk mencari blok "edit" dan menangkap seluruh konfigurasinya
    pattern = r'(edit "(.+?)".+?)(next)'  # Menangkap blok "edit ... next" secara keseluruhan
    matches = re.findall(pattern, config, re.DOTALL)

    # Hanya ambil blok yang mengandung "set ip" atau "set role"
    used_configs = []
    for match in matches:
        block = match[0]
        if 'set ip' in block or 'set role' in block:
            used_configs.append(block + ' next')

    if used_configs:
        return '\n'.join(used_configs)
    else:
        return "No used configurations found."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        config = request.form['config']  # Konfigurasi yang ditempelkan dari textarea
        # Membersihkan konfigurasi dengan hanya menyisakan blok yang digunakan
        filtered_config = filter_used_config(config)
        return render_template('index.html', result=filtered_config, config=config)
    
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)

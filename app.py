from flask import Flask, request, jsonify, render_template, session
import json
import os

app = Flask(__name__, template_folder='.')
app.secret_key = 'rahasia-pkm-genz-2024'

# Kumpulan pertanyaan kuesioner
QUESTIONS = [
    {
        'id': 1,
        'text': 'Seberapa sering Anda membaca berita ekonomi?',
        'options': [
            {'value': 'a', 'label': 'Jarang/tidak pernah'},
            {'value': 'b', 'label': 'Kadang-kadang'},
            {'value': 'c', 'label': 'Rutin setiap hari'}
        ]
    },
    {
        'id': 2,
        'text': 'Apakah Anda pernah mengalami kerugian investasi?',
        'options': [
            {'value': 'a', 'label': 'Belum pernah investasi'},
            {'value': 'b', 'label': 'Pernah, rugi kecil'},
            {'value': 'c', 'label': 'Pernah, paham cara mengatasinya'}
        ]
    },
    {
        'id': 3,
        'text': 'Apa yang Anda lakukan saat saham turun drastis?',
        'options': [
            {'value': 'a', 'label': 'Panik dan jual semua'},
            {'value': 'b', 'label': 'Tahan dulu, lihat perkembangan'},
            {'value': 'c', 'label': 'Analisis dulu sebelum keputusan'}
        ]
    },
    {
        'id': 4,
        'text': 'Apakah Anda tahu cara membaca laporan keuangan?',
        'options': [
            {'value': 'a', 'label': 'Tidak tahu'},
            {'value': 'b', 'label': 'Tahu sedikit'},
            {'value': 'c', 'label': 'Bisa menganalisis'}
        ]
    },
    {
        'id': 5,
        'text': 'Berapa persen dana darurat sebelum investasi?',
        'options': [
            {'value': 'a', 'label': 'Tidak tahu'},
            {'value': 'b', 'label': '< 3 bulan pengeluaran'},
            {'value': 'c', 'label': '≥ 6 bulan pengeluaran'}
        ]
    }
]

# Halaman utama
# Tambahkan ini setelah @app.route('/')
@app.route('/kuisioner')
def kuisioner():
    return render_template('kuisioner.html')

@app.route('/')
def home():
    return render_template('index.html', questions=QUESTIONS)

# API untuk submit jawaban (HANYA SATU FUNCTION INI)
@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    try:
        data = request.json
        answers = data.get('answers', [])
        
        # Hitung skor
        score = 0
        for answer in answers:
            if answer == 'c':
                score += 10
            elif answer == 'b':
                score += 5
            # a = 0
        
        max_score = len(answers) * 10
        if max_score > 0:
            final_score = (score / max_score) * 100
            final_score = round(final_score)
        else:
            final_score = 0
        
        # Dapatkan kategori
        if final_score < 40:
            category = {
                'level': 'pemula',
                'label': '🎓 INVESTOR PEMULA',
                'description': 'Masih perlu belajar dasar-dasar investasi'
            }
        elif final_score < 70:
            category = {
                'level': 'menengah',
                'label': '📊 INVESTOR MENENGAH',
                'description': 'Paham dasar tapi perlu pendalaman risiko'
            }
        else:
            category = {
                'level': 'lanjutan',
                'label': '📈 INVESTOR LANJUTAN',
                'description': 'Pemahaman baik, fokus ke optimalisasi'
            }
        
        # Generate rekomendasi
        if final_score < 40:
            recommendations = {
                'title': 'Mulai dari Dasar',
                'prioritas': [
                    '📘 Belajar apa itu saham dan cara kerjanya',
                    '⚖️ Pahami risiko dasar investasi',
                    '💡 Mulai dengan akun demo trading'
                ]
            }
        elif final_score < 70:
            recommendations = {
                'title': 'Perdalam Analisis',
                'prioritas': [
                    '📊 Pelajari analisis teknikal',
                    '📈 Kuasai analisis fundamental',
                    '🛡️ Terapkan manajemen risiko'
                ]
            }
        else:
            recommendations = {
                'title': 'Optimasi Portofolio',
                'prioritas': [
                    '🎯 Pelajari value investing',
                    '🔄 Atur ulang portofolio (rebalancing)',
                    '🌏 Pahami analisis makroekonomi'
                ]
            }
        
        # Simpan di session
        session['last_result'] = {
            'score': final_score,
            'category': category,
            'recommendations': recommendations
        }
        
        return jsonify({
            'success': True,
            'result': {
                'score': final_score,
                'category': category,
                'recommendations': recommendations
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API untuk ambil hasil terakhir
@app.route('/api/last-result', methods=['GET'])
def last_result():
    result = session.get('last_result', None)
    return jsonify(result)

# Halaman materi edukasi
@app.route('/materi')
def materi():
    return render_template('materi.html')

@app.route('/simulasi')
def simulasi():
    return render_template('simulasi.html')

if __name__ == '__main__':
    app.run(debug=True)
#http://localhost:5000/
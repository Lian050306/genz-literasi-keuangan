# Kategori dan kriteria penilaian
class RiskAssesment:
    def __init__(self):
        self.categories = {
            'pemula': (0, 40, {
                'label': '🎓 Investor Pemula',
                'color': '#ffaa00',
                'description': 'Masih perlu belajar dasar-dasar investasi',
                'risks': ['FOMO', 'Ikut-ikutan', 'Kurang analisis'],
                'action': 'Mulai dari belajar fundamental'
            }),
            'menengah': (41, 70, {
                'label': '📊 Investor Menengah',
                'color': '#4d88ff',
                'description': 'Paham dasar tapi perlu pendalaman risiko',
                'risks': ['Overconfidence', 'Kurang diversifikasi'],
                'action': 'Perdalam analisis teknikal'
            }),
            'lanjutan': (71, 100, {
                'label': '📈 Investor Lanjutan',
                'color': '#00ff88',
                'description': 'Pemahaman baik, fokus ke optimalisasi',
                'risks': ['Complacency', 'Overtrading'],
                'action': 'Pelajari strategi hedging'
            })
        }
    
    def calculate_score(self, answers):
        """Hitung skor dari jawaban kuesioner"""
        score = 0
        max_score = len(answers) * 10  # Misal
        
        # Logika penilaian
        for answer in answers:
            if answer == 'c':  # Jawaban paling paham
                score += 10
            elif answer == 'b':  # Jawaban menengah
                score += 5
            else:  # Jawaban pemula
                score += 0
        
        # Normalisasi ke 0-100
        final_score = (score / max_score) * 100
        return round(final_score)
    
    def get_category(self, score):
        """Dapatkan kategori berdasarkan skor"""
        for range_min, range_max, category in self.categories.values():
            if range_min <= score <= range_max:
                return category
        return self.categories['pemula'][2]  # Default
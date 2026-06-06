from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app) 

db_config = {
    'host': '192.168.56.11',
    'user': 'bukutamu_user',
    'password': 'password123',
    'database': 'bukutamu'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Kelompok 10 Sistem Buku Tamu Digital
# 1. API Login (Mengecek User dan Password)
@app.route('/api/login', methods=['POST'])
def login():
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"message": "Login berhasil", "user_id": user['id'], "username": user['username']}), 200
        else:
            return jsonify({"error": "Username atau password salah!"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# 2. API Registrasi (Mendaftar Akun Baru dengan Batas 10 User)
@app.route('/api/register', methods=['POST'])
def register():
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Cek jumlah pengguna saat ini
        cursor.execute("SELECT COUNT(*) as total FROM users")
        result = cursor.fetchone()
        
        if result['total'] >= 10:
            return jsonify({"error": "Maaf, kuota penuh! Batas maksimal 10 akun telah tercapai."}), 403
            
        # Cek apakah username sudah ada yang pakai
        cursor.execute("SELECT * FROM users WHERE username=%s", (data['username'],))
        if cursor.fetchone():
            return jsonify({"error": "Username sudah terdaftar, silakan pilih nama lain."}), 400
            
        # Simpan user baru ke database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (data['username'], data['password']))
        conn.commit()
        return jsonify({"message": "Akun berhasil dibuat! Silakan login."}), 201
        
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# 3. API Mengambil Data Tamu (Hanya milik User yang sedang Login)
@app.route('/api/tamu/<int:user_id>', methods=['GET'])
def get_tamu(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, nama, instansi, pesan, DATE_FORMAT(waktu_kunjungan, '%Y-%m-%d %H:%i') as waktu FROM daftar_tamu WHERE user_id=%s ORDER BY id DESC"
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        return jsonify(rows)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# 4. API Menyimpan Data Tamu Baru
@app.route('/api/tamu', methods=['POST'])
def add_tamu():
    conn = None
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO daftar_tamu (nama, instansi, pesan, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data['nama'], data['instansi'], data['pesan'], data['user_id']))
        conn.commit()
        return jsonify({"message": "Data Tamu Berhasil Disimpan"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# 5. API Menghapus Data Tamu
@app.route('/api/tamu/<int:id>', methods=['DELETE'])
def delete_tamu(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM daftar_tamu WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return jsonify({"message": "Data berhasil dihapus"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# 6. API Menghapus Akun User (Beserta riwayat datanya)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM daftar_tamu WHERE user_id = %s", (user_id,))
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        return jsonify({"message": "Akun dan semua riwayat berhasil dihapus permanen"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
#  Sistem Buku Tamu Digital Berbasis Cloud (Arsitektur 3 VM)

Proyek ini adalah implementasi Tugas Besar Komputasi Awan oleh **Kelompok 10**. Aplikasi ini merupakan Sistem Buku Tamu Digital interaktif yang dibangun di atas lingkungan Virtualisasi menggunakan Vagrant dan VirtualBox, mengusung arsitektur *Three-Tier* (Frontend, Backend, Database) yang saling terisolasi namun terintegrasi dengan mulus.

## Anggota Kelompok 10
1. Mafud Triyasa Amanullah - [101032400202]
2. [Davindra Chesta Adabi Kuncoro] - [101032400210]
3. [Bhadrika Naufal Suhendi] - [101032400160]

---

##  Fitur Utama Aplikasi
* **Sistem Multi-User:** Mendukung registrasi akun mandiri dengan batasan maksimal 10 pengguna dalam satu sistem.
* **Isolasi Data:** Setiap tamu yang mengisi buku akan dicatat secara spesifik berdasarkan akun pengguna yang sedang *login*.
* **Manajemen Kehadiran (CRUD):** Pengguna dapat membaca daftar tamu yang masuk dan menghapus data riwayat tamu yang sudah tidak relevan.
* **Hapus Akun Mandiri:** Fitur zona berbahaya (*danger zone*) di mana pengguna dapat menghapus akunnya beserta seluruh riwayat tamunya secara permanen melalui verifikasi keamanan lapis dua.
* **UI/UX Modern:** Antarmuka pengguna didesain menggunakan konsep *Glassmorphism*, dilengkapi dengan sistem notifikasi *pop-up* modern (*SweetAlert2*).

---

##  Arsitektur Sistem (3 Virtual Machine)
Sistem ini berjalan di atas sistem operasi dasar **Ubuntu 22.04 (Bento)** dan dibagi menjadi tiga *node* utama:

### 1. VM-Frontend (Web Server)
* **IP Address:** `192.168.56.12` (Port Forwarding: `8080`)
* **Teknologi:** Nginx, HTML5, CSS3, Vanilla JavaScript.
* **Peran:** Menyajikan antarmuka visual aplikasi, mengelola *local storage* untuk sesi *login*, dan mengirimkan permintaan asinkron (Fetch API) ke server *backend*.

### 2. VM-Backend (Application/API Server)
* **IP Address:** `192.168.56.10` (Port Forwarding: `5000`)
* **Teknologi:** Python 3, Flask, Flask-CORS, MySQL Connector.
* **Peran:** Berfungsi sebagai otak logika sistem. Menyediakan *RESTful API* untuk memproses autentikasi pengguna dan manipulasi data dari *frontend*, lalu meneruskannya ke *database*.

### 3. VM-Database (Database Server)
* **IP Address:** `192.168.56.11`
* **Teknologi:** MySQL Server.
* **Peran:** Pusat penyimpanan persisten yang menampung tabel `users` untuk data autentikasi dan tabel `daftar_tamu` untuk riwayat kehadiran.

---

##  Cara Instalasi & Menjalankan Sistem

### Persyaratan Sistem
* [Vagrant](https://www.vagrantup.com/) (Telah terinstal dan berjalan dengan baik)
* [Oracle VM VirtualBox](https://www.virtualbox.org/) (Sebagai *provider* virtualisasi)
* Git

### Langkah-langkah Eksekusi
1. Buka terminal (Command Prompt / PowerShell) dan *clone* repositori ini:
   ```bash
   git clone [URL_GITHUB_REPOSITORI_INI]
   cd [NAMA_FOLDER_REPOSITORI] disini kami mengggunakan : bukutamu
   Nyalakan ketiga Vm secara otomatis [vagrant up]
   Masuk ke dalam Vm Backend untuk dapat menyalakan Application Server [vagrant ssh vm-backend] - [python3 /home/vagrant/app.py], biarkan menyala agar dapat merespon permintaan.
   Buka web di Browser dan akses [http://localhost:8080]
   Sistem telah siap digunakan. -_-


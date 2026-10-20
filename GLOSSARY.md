# Panduan Bahasa Semantic Logging (Versi Membumi & Terukur)

Dokumen ini berisi panduan penulisan `action_narrative` pada log JSON agar mudah dibaca oleh mahasiswa, dosen, maupun pembaca umum.

Gunakan bahasa sehari-hari yang membumi, tetapi **selalu cantumkan perubahan angkanya** dan **hindari kata-kata yang berlebihan/hiperbolik** (seperti: *parah banget, membludak, super cepat*).

---

## 1. Kata Kerja Proses Utama (Action Verbs)

Gunakan istilah proses sehari-hari yang sudah biasa dipakai saat ngoding:

* **Inisialisasi / Setup (`INITIALIZE`)**: Persiapan awal graf dan variabel.
  * *Contoh:* `"Set jarak awal Pos Damkar (Node 0) = 0, node lainnya = infinity."`
* **Cek Tetangga (`EVALUATE`)**: Memeriksa jalan/gang yang terhubung dari posisi saat ini.
  * *Contoh:* `"Mengecek jalan dari Node 0 ke Node 2 (Gang B) dengan jarak 2 meter."`
* **Perbarui Jarak (`RELAX / UPDATE`)**: Menemukan jalan yang lebih cepat/pendek.
  * *Contoh:* `"Jarak ke Simpang (Node 3) diperbarui dari infinity menjadi 3 meter lewat Gang B."`
* **Ubah Bobot Jalan (`UPDATE_WEIGHT`)**: Perubahan kondisi jalan akibat kejadian di lapangan.
  * *Contoh:* `"Bobot Gang B (Edge 2 -> 3) naik dari 1 menjadi 50 karena ada kerumunan warga."`
* **Hitung Ulang Rute (`RECALCULATE`)**: Algoritma mencari jalan memutar karena rute lama tersumbat.
  * *Contoh:* `"Rute lama tersumbat. Algoritma menghitung ulang rute dari Pos Damkar."`
* **Rute Ditemukan (`PATH_FOUND`)**: Jalur terbaik sudah didapatkan.
  * *Contoh:* `"Rute terbaik ditemukan: [0, 1, 3, 4] dengan total jarak 10 meter."`

---

## 2. Contoh Perbandingan Kalimat Log

Berikut adalah contoh cara merubah kalimat agar membumi namun tetap terukur:

### Kasus 1: Hambatan Kerumunan Warga

* ❌ **Terlalu Kaku/Akademis:** `"INJECT_SPATIAL_PENALTY on edge (2, 3): Weight updated from 1.0 to 50.0."`
* ❌ **Hiperbolik:** `"Gang B macet parah banget gara-gara penonton membludak!"`
* ✅ **Membumi & Terukur:** `"Bobot Gang B (Edge 2 -> 3) naik dari 1 jadi 50 karena kerumunan warga. Algoritma menghitung ulang rute."`

### Kasus 2: Penemuan Rute Baru

* ❌ **Terlalu Kaku/Akademis:** `"RECONSTRUCT_PATH yields sequence [0, 1, 3, 4] with accumulated_cost=10.0."`
* ❌ **Hiperbolik:** `"Damkar berhasil menemukan rute ajaib yang super cepat melompati kemacetan!"`
* ✅ **Membumi & Terukur:** `"Rute baru dipilih memutar lewat Gang A [0, 1, 3, 4] dengan total waktu 10 menit (lebih cepat dibanding lewat Gang B yang totalnya 54 menit)."`

---

## 3. Aturan Sederhana untuk Mahasiswa

1. **Gunakan Bahasa Indonesia / Inggris Santai yang Jelas.**
2. **Sebutkan Nama Tempatnya:** Gunakan label tempat seperti `Pos Damkar`, `Gang A`, bukan cuma `Node 0`.
3. **Selalu Tulis Angkanya:** Jangan cuma bilang *"jaraknya bertambah"*, tapi tulis *"jarak naik dari 2 jadi 50"*.

## 4. Contoh System Prompt untuk Gemini
```
  Kamu adalah asisten pengajar Matematika Diskrit. Berikut adalah data JSON hasil trace algoritma Dijkstra (kuantitatif) dan file YAML skenario. Tolong buatkan kolom action_narrative di setiap step menggunakan bahasa Indonesia yang membumi, komunikatif, sebutkan nama tempatnya dari label YAML, dan sebutkan perubahan angkanya tanpa kata-kata hiperbolik.
```


# CASESS

## 📋 Daftar Kasus Tugas Besar

| Kelompok / Case ID | Title Kasus Skenario | Ringkasan Dinamika Event Injection |
| --- | --- | --- |
| `case_01` | `case_01_kobra_banjir.yaml` | Ular kobra muncul di Gang B akibat banjir, menutup rute. |
| `case_02` | `case_02_hajatan_tenda.yaml` | Tenda pernikahan warga memblokir koridor/jalan utama. |
| `case_03` | `case_03_pohon_tumbang.yaml` | Pohon tumbang akibat angin kencang menutup akses lorong. |
| `case_04` | `case_04_pasar_tumpah.yaml` | Pedagang pasar tumpah meluap ke persimpangan jalan. |
| `case_05` | `case_05_tawuran_pelajar.yaml` | Tawuran pelajar memblokir titik simpul pertigaan. |
| `case_06` | `case_06_perbaikan_drainase.yaml` | Galian gorong-gorong membuat bobot rute melonjak drastis. |
| `case_07` | `case_07_truk_mogok.yaml` | Truk muatan mogok di persimpangan jalan memicu kemacetan. |
| `case_08` | `case_08_warga_nonton.yaml` | Kerumunan warga menonton kebakaran menutup jalan tembus. |
| `case_09` | `case_09_kebocoran_gas.yaml` | Kebocoran tabung gas Elpiji menutup akses area dapur/koridor. |
| `case_10` | `case_10_pawai_obor.yaml` | Rombongan pawai menutup jalur utama secara bergantian. |
| `case_11` | `case_11_korsleting_panel.yaml` | Ledakan panel listrik memicu titik api lokal di koridor. |
| `case_12` | `case_12_genangan_oli.yaml` | Tumpahan oli di persimpangan membuat jalur sangat licin/berbahaya. |
| `case_13` | `case_13_kucing_terjebak.yaml` | Warga berkerumun menyelamatkan kucing di tangga darurat. |
| `case_14` | `case_14_gapura_roboh.yaml` | Gapura 17-an roboh menutup akses gerbang utama. |
| `case_15` | `case_15_pintu_sekat_terkunci.yaml` | Pintu sekat otomatis terkunci karena false alarm. |
| `case_16` | `case_16_tawon_vespa.yaml` | Sarang tawon vespa mengamuk di lorong penghubung. |
| `case_17` | `case_17_karnaval_sepeda.yaml` | Konvoi anak-anak karnaval memadati lorong gedung. |
| `case_18` | `case_18_material_bangunan.yaml` | Tumpukan pasir dan batu bata menutupi sebagian koridor. |
| `case_19` | `case_19_parkir_liar.yaml` | Motor parkir sembarangan mempersempit lebar efektif lorong. |
| `case_20` | `case_20_asap_sate.yaml` | Kepulan asap pembakaran sate tebal mengganggu visibilitas. |
| `case_21` | `case_21_anjing_galak.yaml` | Anjing penjaga lepas di area persimpangan rute. |
| `case_22` | `case_22_posyandu_meluap.yaml` | Antrean Posyandu meluber hingga memblokir lorong utama. |
| `case_23` | `case_23_tumpahan_cat.yaml` | Cat tembok tumpah menutup jalur di dekat tangga darurat. |
| `case_24` | `case_24_kabel_putus.yaml` | Kabel PLN putus melintang di tengah persimpangan. |
| `case_25` | `case_25_rombongan_besan.yaml` | Rombongan keluarga pengantin berjalan lambat memenuhi jalan. |
| `case_26` | `case_26_gudang_terbakar.yaml` | Penyebaran asap tebal dari area gudang ke koridor utama. |
| `case_27` | `case_27_ambulans_masuk.yaml` | Penutupan sementara koridor untuk evakuasi medis emergency. |
| `case_28` | `case_28_siskamling_portal.yaml` | Portal siskamling ditutup warga karena ada isu maling. |

---

## 🗺️ Matriks Pemetaan 28 Kasus Skenario & Algoritma Solusi

Berikut adalah **Matriks Pemetaan 28 Kasus Skenario Tugas Besar** ke dalam **4 Kategori Algoritma Utama** (Pathfinding, Max Flow, Spanning Tree, dan Graph Coloring).

Pemetaan ini dirancang agar setiap kelompok mahasiswa D4 mendapatkan konteks cerita lokal yang unik dan sesuai dengan karakteristik algoritma yang dipelajarinya:

### Kategori 1: Pathfinding / Dynamic Rerouting (Dijkstra / D* Lite)

> **Fokus**: Mencari rute terpendek/teraman dari titik *start* ke *goal* saat jalur mengalami perubahan bobot/penutupan akibat rintangan dinamis.

| Kelompok / Case ID | Title Kasus Skenario | Cerita & Alasan Pemetaan Algoritma |
| --- | --- | --- |
| **`case_01`** | `case_01_kobra_banjir.yaml` | **Luapan air membawa Ular Kobra di Gang B**: Bobot jalur melonjak drastis, memaksa Dijkstra menghitung ulang rute memutar via Gang A. |
| **`case_02`** | `case_02_hajatan_tenda.yaml` | **Tenda Pernikahan Warga**: Jalan utama tertutup total (bobot `W = ∞`), menuntut pencarian rute alternatif tercepat melalui gang sempit. |
| **`case_03`** | `case_03_pohon_tumbang.yaml` | **Pohon Angsana Tumbang**: Menutup akses jalan protokol, memicu *dynamic rerouting* saat simulasi pergerakan sedang berjalan. |
| **`case_06`** | `case_06_perbaikan_drainase.yaml` | **Galian Gorong-gorong**: Bobot waktu tempuh meningkat akibat pembongkaran jalan, membutuhkan evaluasi rute terpendek baru. |
| **`case_08`** | `case_08_warga_nonton.yaml` | **Kerumunan Warga Nonton Kebakaran**: Kerumunan memblokir jalan tembus, memerlukan kalkulasi rute memutar (*baseline Dijkstra testcase*). |
| **`case_11`** | `case_11_korsleting_panel.yaml` | **Ledakan Panel Listrik**: Memicu titik api lokal di koridor utama, memaksa pejalan kaki berbalik arah mencari pintu darurat lain. |
| **`case_14`** | `case_14_gapura_roboh.yaml` | **Gapura 17-an Roboh**: Akses gerbang utama tertutup, mengharuskan pengalihan jalur ke pintu samping gedung/kawasan. |

---

### Kategori 2: Maximum Flow / Bottleneck Analysis (Ford-Fulkerson / Dinic's)

> **Fokus**: Menghitung kapasitas maksimum aliran massa/kendaraan dari titik *source* ke *sink* serta mendeteksi titik penyempitan (*bottleneck*).

| Kelompok / Case ID | Title Kasus Skenario | Cerita & Alasan Pemetaan Algoritma |
| --- | --- | --- |
| **`case_04`** | `case_04_pasar_tumpah.yaml` | **Pasar Tumpah Subuh**: Lapak pedagang mengurangi lebar efektif koridor jalan, menurunkan *max flow* evakuasi secara drastis. |
| **`case_07`** | `case_07_truk_mogok.yaml` | **Truk Muatan Mogok**: Menyebabkan penyempitan (*bottleneck*) di persimpangan, membatasi jumlah kendaraan/massa yang bisa lewat per menit. |
| **`case_17`** | `case_17_karnaval_sepeda.yaml` | **Konvoi Karnaval Sepeda**: Memenuhi kapasitas koridor lorong, memicu penumpukan massa di pintu keluar (*exit discharge*). |
| **`case_19`** | `case_19_parkir_liar.yaml` | **Deretan Parkir Liar Motor**: Mempersempit kapasitas jaringan lorong evakuasi gedung, diuji dengan algoritma Max Flow. |
| **`case_22`** | `case_22_posyandu_meluap.yaml` | **Antrean Posyandu Meluber**: Antrean ibu dan balita memenuhi lorong, mengurangi *throughput* aliran evakuasi darurat. |
| **`case_25`** | `case_25_rombongan_besan.yaml` | **Rombongan Pengantin**: Arus rombongan yang berjalan lambat membatasi kapasitas maksimum jalur koridor utama. |
| **`case_27`** | `case_27_ambulans_masuk.yaml` | **Evakuasi Medis Emergency**: Penutupan parsial koridor untuk alur kerek tabung/stretcher, memicu penyempitan kapasitas *sink*. |

---

### Kategori 3: Minimum Spanning Tree / Network Connectivity (Prim's / Kruskal's)

> **Fokus**: Menghubungkan seluruh nodus (sensor/pos/posko) dengan total bobot (panjang kabel/jarak/daya) minimum serta menjaga konektivitas jaringan.

| Kelompok / Case ID | Title Kasus Skenario | Cerita & Alasan Pemetaan Algoritma |
| --- | --- | --- |
| **`case_09`** | `case_09_kebocoran_gas.yaml` | **Kebocoran Gas Elpiji**: Mengharuskan pemasangan jaringan sensor gas darurat untuk menghubungkan seluruh pos pantau dengan kabel minimum. |
| **`case_15`** | `case_15_pintu_sekat_terkunci.yaml` | **Sistem Pintu Sekat Terkunci**: Memerlukan re-koneksi jaringan sinyal kontrol *fire door* antar ruangan agar tetap terhubung ke panel pusat. |
| **`case_18`** | `case_18_material_bangunan.yaml` | **Tumpukan Bahan Bangunan**: Memutus jalur kabel utama, memerlukan penghitungan ulang pohon rentang minimum (MST) untuk jalur komunikasi. |
| **`case_23`** | `case_23_tumpahan_cat.yaml` | **Tumpahan Cat di Jalur Kabel**: Merusak nodus sensor lantai, menuntut *self-healing network* menggunakan algoritma Kruskal. |
| **`case_24`** | `case_24_kabel_putus.yaml` | **Kabel Sirkuit Utama Putus**: Memutus jaringan *fire alarm* antar gedung, membutuhkan pembentukan topologi MST baru. |
| **`case_26`** | `case_26_gudang_terbakar.yaml` | **Kebakaran Area Gudang**: Nodus sensor gudang terbakar, sistem merutekan ulang *backbone mesh network* sensor yang selamat. |
| **`case_28`** | `case_28_siskamling_portal.yaml` | **Penutupan Portal Siskamling**: Menghubungkan seluruh pos ronda/HT warga dengan total jangkauan komunikasi terpendek. |

---

### Kategori 4: Graph Coloring / Conflict Scheduling (DSATUR / Greedy Coloring)

> **Fokus**: Menghindari benturan/konflik pada nodus atau persimpangan yang berdekatan dengan mengalokasikan slot waktu (*color/time-slot*) yang berbeda.

| Kelompok / Case ID | Title Kasus Skenario | Cerita & Alasan Pemetaan Algoritma |
| --- | --- | --- |
| **`case_05`** | `case_05_tawuran_pelajar.yaml` | **Tawuran di Simpul Pertigaan**: Mengatur alokasi giliran alur evakuasi kelompok massa dari arah berlawanan agar tidak bertabrakan. |
| **`case_10`** | `case_10_pawai_obor.yaml` | **Pawai Obor Warga**: Mengatur *scheduling* jadwal giliran melintas di persimpangan lorong agar tidak terjadi penumpukan. |
| **`case_12`** | `case_12_genangan_oli.yaml` | **Tumpahan Oli di Persimpangan**: Mengatur giliran evakuasi per kelompok (*phase allocation*) agar massa tidak berjejalan di titik licin. |
| **`case_13`** | `case_13_kucing_terjebak.yaml` | **Kerumunan Evakuasi Kucing**: Mengatur jadwal penggunaan tangga darurat yang saling bersilangan antar lantai. |
| **`case_16`** | `case_16_tawon_vespa.yaml` | **Sarang Tawon Vespa Mengamuk**: Mengalokasikan *time-slot* giliran lewat lorong agar evakuasi dilakukan secara bertahap (bergantian). |
| **`case_20`** | `case_20_asap_sate.yaml` | **Asap Pembakaran Sate**: Mengatur giliran pelepasan gelombang evakuasi warga di persimpangan agar visibilitas tetap aman. |
| **`case_21`** | `case_21_anjing_galak.yaml` | **Anjing Penjaga Lepas**: Mengatur alokasi zonasi pergerakan warga agar tidak bentrok dengan area jelajah anjing di persimpangan. |

---

## 📌 Ringkasan Distribusi Pembagian 28 Kelompok

* **Pathfinding (Dijkstra / D* Lite)**: Case 01, 02, 03, 06, 08, 11, 14 (7 Kelompok)
* **Max Flow (Ford-Fulkerson / Dinic)**: Case 04, 07, 17, 19, 22, 25, 27 (7 Kelompok)
* **Spanning Tree (Kruskal / Prim)**: Case 09, 15, 18, 23, 24, 26, 28 (7 Kelompok)
* **Graph Coloring (Greedy / DSATUR)**: Case 05, 10, 12, 13, 16, 20, 21 (7 Kelompok)

```text
cases/scenarios/
├── case_01_kobra_banjir.yaml         (Pathfinding - Dijkstra/D*)
├── case_02_hajatan_tenda.yaml        (Pathfinding - Dijkstra/D*)
├── case_03_pohon_tumbang.yaml        (Pathfinding - Dijkstra/D*)
├── case_04_pasar_tumpah.yaml         (Max Flow - Ford-Fulkerson/Dinic)
├── case_05_tawuran_pelajar.yaml      (Graph Coloring - DSATUR/Greedy)
├── case_06_perbaikan_drainase.yaml   (Pathfinding - Dijkstra/D*)
├── case_07_truk_mogok.yaml           (Max Flow - Ford-Fulkerson/Dinic)
├── case_08_warga_nonton.yaml         (Pathfinding - Dijkstra/D*)
├── case_09_kebocoran_gas.yaml        (Spanning Tree - Kruskal/Prim)
├── case_10_pawai_obor.yaml           (Graph Coloring - DSATUR/Greedy)
├── case_11_korsleting_panel.yaml     (Pathfinding - Dijkstra/D*)
├── case_12_genangan_oli.yaml         (Graph Coloring - DSATUR/Greedy)
├── case_13_kucing_terjebak.yaml      (Graph Coloring - DSATUR/Greedy)
├── case_14_gapura_roboh.yaml         (Pathfinding - Dijkstra/D*)
├── case_15_pintu_sekat_terkunci.yaml (Spanning Tree - Kruskal/Prim)
├── case_16_tawon_vespa.yaml          (Graph Coloring - DSATUR/Greedy)
├── case_17_karnaval_sepeda.yaml      (Max Flow - Ford-Fulkerson/Dinic)
├── case_18_material_bangunan.yaml    (Spanning Tree - Kruskal/Prim)
├── case_19_parkir_liar.yaml          (Max Flow - Ford-Fulkerson/Dinic)
├── case_20_asap_sate.yaml            (Graph Coloring - DSATUR/Greedy)
├── case_21_anjing_galak.yaml         (Graph Coloring - DSATUR/Greedy)
├── case_22_posyandu_meluap.yaml      (Max Flow - Ford-Fulkerson/Dinic)
├── case_23_tumpahan_cat.yaml         (Spanning Tree - Kruskal/Prim)
├── case_24_kabel_putus.yaml          (Spanning Tree - Kruskal/Prim)
├── case_25_rombongan_besan.yaml      (Max Flow - Ford-Fulkerson/Dinic)
├── case_26_gudang_terbakar.yaml      (Spanning Tree - Kruskal/Prim)
├── case_27_ambulans_masuk.yaml       (Max Flow - Ford-Fulkerson/Dinic)
└── case_28_siskamling_portal.yaml    (Spanning Tree - Kruskal/Prim)
```

---

## 📚 Referensi

| Domain | Penulis Awal Klasik | Penulis Awal SOTA Modern |
| --- | --- | --- |
| Pathfinding | Dijkstra (1959) | Hart et al. / A* (1968) & Koenig & Likhachev / D* Lite (2002) |
| Max-Flow | Ford & Fulkerson (1956) | Goldberg & Tarjan / Push-Relabel (1988) & Boykov-Kolmogorov / BK (2004) |
| Spanning Tree | Kruskal (1956) / Prim (1957) | Holm, de Lichtenberg & Thorup / HLT Dynamic MST (2001) |
| Coloring | Matula et al. / Greedy (1972) | Brélaz / DSATUR (1979) & Mehrotra & Trick / Column Generation (1996) |
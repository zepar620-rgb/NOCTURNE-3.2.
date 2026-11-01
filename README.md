# ✠ NOCTURNE 3.2 — Android APK Project

Paket ini membungkus **aplikasi Python Flask NOCTURNE 3.2** menjadi aplikasi Android native shell menggunakan Android WebView + Chaquopy. Backend Python, scraper, API provider, UI Gothic, SQLite, multi-source search, MAL/Tenrai, AniList, Kitsu, AniPub, MiteNime, AniMap, ANN, dan player yang sudah ada tetap menjadi inti aplikasi.

> **Status paket:** project Android siap dibuild. APK biner belum disertakan karena lingkungan pembuatan file tidak memiliki Android SDK/Gradle dan akses internet untuk mengunduh dependency build. Gunakan Android Studio atau workflow GitHub Actions di bawah untuk menghasilkan APK debug.

## Yang ada di dalam APK

- Python 3.13 dijalankan di dalam proses aplikasi Android melalui Chaquopy.
- Flask berjalan lokal pada `127.0.0.1:8765`; server tidak dibuka ke jaringan Wi-Fi/LAN.
- WebView Android menampilkan seluruh UI NOCTURNE 3.2.
- Player `target=_blank` dibuka pada jendela WebView terpisah di dalam aplikasi, agar host yang menolak iframe bisa dibuka sebagai halaman tingkat atas.
- Video fullscreen didukung melalui WebChromeClient.
- Form impor backup memakai Android document picker.
- Ekspor backup JSON memakai endpoint unduhan khusus Android dan DownloadManager.
- Database `nocturne.db` disimpan di direktori privat aplikasi, sehingga tidak perlu Termux atau Termux:X11.
- Status bar, navigation bar, splash loading, ikon, dan tema native memakai palet Gothic Crimson.

## Persyaratan build

- Android Studio versi terbaru yang mendukung AGP 8.13.x, atau build melalui GitHub Actions.
- JDK 17.
- Android SDK Platform 36 dan Build Tools 36.0.0.
- Python 3.13 pada mesin build (dibutuhkan Chaquopy untuk menyiapkan paket pip).
- Gradle 8.13.
- Internet saat build pertama untuk mengunduh Gradle, Android Gradle Plugin, Chaquopy, Python runtime dan wheel dependencies.

Konfigurasi project: AGP `8.13.2`, Chaquopy `17.2.0`, Gradle `8.13`, Python `3.13`, `minSdk 24`, target SDK `35`. Chaquopy mewajibkan minSdk 24 pada versi 17.2 dan mendukung ABI `arm64-v8a` serta `x86_64`.

## Build dengan Android Studio

1. Ekstrak `NOCTURNE_3_2_ANDROID.zip`.
2. Android Studio → **Open** → pilih folder `NOCTURNE_3_2_ANDROID` (folder yang berisi `settings.gradle`).
3. Atur Gradle JDK ke **JDK 17** pada Settings → Build Tools → Gradle.
4. Pastikan SDK Platform 36 terpasang melalui SDK Manager.
5. Tunggu Gradle Sync selesai dan izinkan Android Studio mengunduh komponen yang diminta.
6. Pilih **Build → Build Bundle(s) / APK(s) → Build APK(s)**.
7. APK debug akan berada di:

```text
app/build/outputs/apk/debug/app-debug.apk
```

Nama aplikasi pada launcher: `NOCTURNE 3.2`.

## Build melalui command line

Setelah JDK, Python, Gradle, dan Android SDK terpasang serta `ANDROID_HOME` diatur:

```bash
./build_apk.sh
```

Perintah yang dijalankan oleh script:

```bash
gradle --no-daemon --stacktrace assembleDebug
```

## Build APK melalui GitHub Actions (tanpa Android Studio lokal)

Workflow telah disediakan pada `.github/workflows/build-apk.yml`.

1. Buat repository GitHub baru.
2. Upload seluruh isi folder project ini ke repository tersebut.
3. Buka tab **Actions**.
4. Pilih **Build NOCTURNE Android APK**.
5. Tekan **Run workflow** dan tunggu job build selesai.
6. Buka hasil run, lalu unduh artifact `NOCTURNE-3.2-debug-APK`.
7. Ekstrak artifact; file di dalamnya adalah `app-debug.apk`.

Workflow membangun APK debug yang ditandatangani debug key. Untuk publikasi Play Store, buat konfigurasi release dan signing key pribadi sendiri. Jangan memasukkan keystore atau password signing ke repository publik.

## Penyimpanan dan migrasi data

- APK menyimpan database di direktori privat aplikasi: `files/nocturne.db`.
- Database tidak memakai direktori Python source yang read-only di dalam APK.
- Data di APK terpisah dari `nocturne.db` versi Termux. Untuk migrasi, ekspor backup JSON dari versi lama lalu impor melalui menu **Tools & Backup** di APK.
- Menghapus data aplikasi atau uninstall dapat menghapus database privat. Ekspor backup berkala.

## Catatan player dan WebView

- Player yang mengizinkan embedding akan tetap tampil di dalam halaman episode.
- Tombol player eksternal yang membuka `target=_blank` ditangkap sebagai jendela WebView terpisah di dalam APK. Ini membuat URL player menjadi top-level document, bukan iframe di halaman Otakudesu.
- Server video tetap dapat menolak koneksi, mensyaratkan browser eksternal, membatasi wilayah, atau memerlukan kebijakan/JavaScript yang tidak kompatibel dengan WebView. APK tidak membypass DRM, login, anti-bot, atau kebijakan embedding.
- Hasil playback tergantung perangkat, codec, koneksi, host video, dan WebView Android.

## Privasi dan keamanan

- Flask hanya bind ke `127.0.0.1`, bukan `0.0.0.0`.
- Aplikasi meminta permission INTERNET untuk katalog/API dan pemutar video eksternal.
- WebView menjalankan JavaScript karena UI NOCTURNE menggunakan JavaScript.
- `usesCleartextTraffic` diaktifkan agar WebView dapat berkomunikasi dengan server loopback HTTP lokal. Jangan mengubah host server menjadi alamat LAN/public tanpa menambahkan autentikasi dan perlindungan yang sesuai.
- Aplikasi menampilkan konten pihak ketiga dari katalog/API/video host. Ikuti ketentuan tiap penyedia.

## Berkas penting

```text
NOCTURNE_3_2_ANDROID/
├── app/
│   ├── build.gradle
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/nocturne/archive/MainActivity.java
│       ├── python/
│       │   ├── nocturne_android.py
│       │   └── otakudesu_gothic.py
│       └── res/
├── .github/workflows/build-apk.yml
├── build.gradle
├── build_apk.sh
├── settings.gradle
└── README.md
```

## Pemeriksaan yang sudah dilakukan pada paket ini

- Sintaks Python pada scraper utama dan bridge Android.
- Pemeriksaan XML manifest, theme, dan ikon.
- Pemeriksaan struktur project dan ZIP.

Build Gradle penuh dan pengujian di perangkat Android belum dijalankan di lingkungan ini karena Android SDK/Gradle dependency tidak tersedia dan jaringan build eksternal tidak dapat diakses.

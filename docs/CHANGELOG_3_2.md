# NOCTURNE 3.2 — Multiverse Archive

## Fitur baru

- Multi-source search paralel: MyAnimeList data melalui Tenrai, AniList, Kitsu, AniPub, MiteNime, AniMap, dan Anime News Network Encyclopedia.
- Multi-source dossier untuk AniList, Kitsu, AniPub, MiteNime, AniMap, Tenrai, dan ANN.
- AniList character / Japanese VA cards dan recommendation cards pada dossier.
- Discovery Hub menggabungkan AniList trending, MAL popularity, dan AniPub top-rated.
- Random anime via Tenrai.
- Airing Calendar via AniList GraphQL.
- Anime News feed via Tenrai.
- API Monitor untuk mengecek tujuh provider dari perangkat Termux.
- Cache, timeout, throttling per provider, penanganan 429/403/5xx, dan hasil parsial jika salah satu provider gagal.
- Provider API menggunakan session tanpa automatic retry; pemanggilan publik dibatasi sesuai panduan provider.

## Dipertahankan

- Otakudesu public-page scraper, katalog, ongoing, jadwal, genre, pencarian, detail, episode.
- Embedded + external player, poster, navigasi episode.
- MyAnimeList via Tenrai (public catalogue), local library SQLite, watch history, JSON backup.
- Gothic Crimson responsive UI dan layout scroll.

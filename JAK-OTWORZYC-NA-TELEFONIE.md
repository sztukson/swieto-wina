# 🍷 Święto Wina — wersja na telefon i tablet

## 🔗 Link (działa na każdym telefonie/tablecie)
**https://sztukson.github.io/swieto-wina/**

Albo zeskanuj **QR-link.png** aparatem.

---

## 📲 Jak zainstalować jako aplikację (ikona na ekranie)

### iPhone / iPad (Safari)
1. Otwórz link w **Safari**
2. Kliknij przycisk **Udostępnij** (kwadrat ze strzałką ⬆️)
3. **„Do ekranu początkowego"** → **Dodaj**
4. Pojawi się ikona 🍷 jak normalna apka — działa też offline

### Android (Chrome)
1. Otwórz link w **Chrome**
2. Menu **⋮** (trzy kropki) → **„Zainstaluj aplikację"** / „Dodaj do ekranu głównego"
3. Ikona 🍷 ląduje na ekranie

---

## ✨ Co nowego w wersji mobilnej (vs Mac)
- **☀️/🌙 Tryb dzienny** — przycisk w prawym górnym rogu. Na słońcu włącz jasny, wieczorem ciemny. Wybór się zapamiętuje.
- **Prostsza nawigacja** — 5 głównych zakładek + **⋯ Więcej** (Baza, Dni, Log, AI, Eksport, Ustawienia)
- **Wibracja** przy kliknięciu sprzedaży (potwierdzenie dotykiem)
- **Większe napisy** na ekranach dotykowych
- **Działa offline** — bez internetu apka się otworzy, dane zapiszą lokalnie i zsynchronizują gdy wróci sieć

## 🔑 Logowanie
To samo konto co na Macu (e-mail + hasło). Te same dane, ta sama baza — wszyscy widzą to samo.
Bez internetu: **„📴 Tryb offline"** na ekranie logowania.

---

## 🔄 Jak zaktualizować apkę w przyszłości
Pliki są w tym folderze + repo GitHub `sztukson/swieto-wina`.
Po zmianie `index.html`:
```
cd "aplikacja na telefon i tablet"
git add -A && git commit -m "update" && git push
```
Zmiana pojawi się na linku po ~1 min. (W service-worker.js podbij `swieto-wina-v1` → `v2`, żeby telefony pobrały nową wersję.)

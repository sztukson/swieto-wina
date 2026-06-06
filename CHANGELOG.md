# Święto Wina — historia wersji

Schemat: **vMAJOR.MINOR** (produkt) + **build N** (numer wdrożenia, do diagnozy cache).
- MAJOR — duża zmiana koncepcji/UX (np. przejście na kafelki).
- MINOR — nowe funkcje, poprawki.
- build — rośnie z każdym deployem; widoczny na dole apki.

---

## v1.0 (build 20) — 2026-06-06 — pierwsza wersja telefon/tablet (PWA)
- Model sprzedaży **kafelki**: wino → rodzaj (degustacja/butelka) → płatność (gotówka/karta/BLIK) → rabat (tylko butelka: −5%/−10%/własny %/zł)
- Kafelki równe, pełne nazwy (zawijanie bez obcinania), kolory wg koloru wina
- Pasek „↩️ Cofnij" ostatnich akcji
- Filtr koloru wina + szukajka
- **Podsumowanie** (była Kasa): degustacje/butelki/przychód/kaucje/kasa stan oczekiwany/stan początkowy + operacje wpłata/wypłata (bez liczenia banknotów)
- **Baza win**: dodawanie i usuwanie win (synchronizacja Supabase)
- Nawigacja: Wina · Kieliszki · Podsumowanie · Statsy · Więcej (Baza/Dni/Transport/Ustawienia)
- PWA: offline (service worker), instalacja na ekranie głównym, tryb dzień/noc, auto-reload przy aktualizacji
- Hosting: GitHub Pages — https://sztukson.github.io/swieto-wina/

## Wersja Mac (Electron .dmg) — równolegle
- Pełna apka z liczeniem banknotów (Kasa), dla głównych stanowisk
- Dostała dodawanie/usuwanie win (build 20)
- Ta sama baza Supabase co PWA

# Święto Wina — historia wersji

Schemat: **vMAJOR.MINOR** (produkt) + **build N** (numer wdrożenia, do diagnozy cache).
- MAJOR — duża zmiana koncepcji/UX (np. przejście na kafelki).
- MINOR — nowe funkcje, poprawki.
- build — rośnie z każdym deployem; widoczny na dole apki.

---

## v1.1 (build 21) — 2026-08-06 — wersja stabilna po naprawie synchronizacji i bezpieczenstwa

**To jest oznaczona wersja dzialajaca (tag `v1.1`).** Sprawdzone: 5 dni w archiwum,
1317 operacji w logu, RLS na wszystkich 5 tabelach, Advisor 0 bledow.

### Naprawione
- **Stare dane wracaly mimo zapisanych dni.** `sbPushLive` stemplowal snapshot
  znacznikiem `_opTs = SB_LASTOP` (czas ostatniej operacji). Gdy nikt nic nie
  klika, ta wartosc stoi w miejscu, wiec kolejne snapshoty mialy identyczny
  znacznik, a warunek przyjecia byl `>=` — kazde logowanie i kazdy `sync-full`
  przyjmowaly stary stan. Teraz znacznik to rosnacy zegar, a snapshot jest
  przyjmowany tylko gdy faktycznie nowszy (`>`).
- **Odswiezanie po kliknieciu w trakcie logowania.** `controllerchange` z service
  workera przeladowywal strone natychmiast, takze gdy user wpisywal haslo.
  Teraz przeladowanie czeka az ekran logowania i okna beda zamkniete, zadne pole
  nie jest aktywne, a karta jest widoczna.

### Bezpieczenstwo bazy (Supabase)
- Wlaczony **Row-Level Security** na `days`, `wines`, `live_state`, `ops`,
  `allowed_users`. Wczesniej RLS byl wylaczony, a rejestracja jest otwarta —
  kazdy kto zalozyl konto mial pelny dostep do wszystkiego. Dostep ma teraz
  wylacznie mail z `allowed_users`; zapis do listy uzytkownikow tylko admin.
- Nowe tabele dostaja RLS i domyslna polityke automatycznie (trigger `ensure_rls`).
- Zrodlo prawdy: `rls-fix.sql` w folderze projektu (idempotentny).

### Wczesniej niewpisane do changeloga (weszly miedzy build 20 a 21)
- Kieliszki w statystykach: sprzedaz godzinowa (filtr + slupek) i dashboard
- Korekta magazynu: podglad −N butelek, powod „pomylka" domyslny
- Kieliszek w pickerze kafelkow (tablet/telefon)

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

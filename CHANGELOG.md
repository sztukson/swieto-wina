# Święto Wina — historia wersji

Schemat: **vMAJOR.MINOR** (produkt) + **build N** (numer wdrożenia, do diagnozy cache).
- MAJOR — duża zmiana koncepcji/UX (np. przejście na kafelki).
- MINOR — nowe funkcje, poprawki.
- build — rośnie z każdym deployem; widoczny na dole apki.

---

## v1.2 (build 22) — 2026-08-06 — offline na komputerze + wiadomo kto liczyl

**Wersja komputerowa dziala teraz offline i da sie ja zainstalowac.** Wczesniej
`/desktop/` byla jedyna wersja bez service workera i manifestu — czyli bez
internetu nie otwierala sie w ogole. Teraz w Chrome mozna kliknac „Zainstaluj"
i dostac osobne okno w Docku, dzialajace bez sieci. Bez .dmg, bez Gatekeepera.

### Offline z zachowaniem tozsamosci (najwazniejsze)
Wczesniej brak internetu wygladal jak brak uprawnien: `sbCheckAccess` odpytywal
`allowed_users`, zapytanie padalo i user (poza adminem, ktory ma fallback)
dostawal ekran „⛔ Brak dostepu". A jesli wszedl przyciskiem „Tryb offline",
to operacje szly do kolejki **bez podpisu** (`entry.by = null`) i nigdy sie nie
wysylaly. Zmiany:
- po kazdym udanym sprawdzeniu dostepu zapisujemy decyzje lokalnie (`sw_access`),
  a gdy siec nie odpowiada — wpuszczamy na jej podstawie (pasek 📴 OFFLINE)
- „Tryb offline" **pyta, kto liczy**, i tym podpisuje kazda operacje; podpis
  jest pamietany, wiec przy kolejnym otwarciu bez sieci apka nie pyta ponownie
- kolejka (`sw_outbox`) ma komu przypisac operacje, wiec po powrocie sieci /
  zalogowaniu sama je dosyła — sprawdzone end-to-end na prawdziwej bazie
- w logu zostaje: **kto** (`by`), **dokladna godzina kliknięcia** (`ts`) i
  znacznik **📴 offline**; osobno w bazie widac godzine wyslania (`created_at`)
- brak sieci nie pokazuje sie juz jako „⚠️ BLAD SYNC" (nowe `srvProblem()`)

Bezpieczenstwo bez zmian: prawdziwa brama to RLS w bazie, wiec operacje osoby
usunietej z `allowed_users` zostana odrzucone przy synchronizacji.

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


## Wersja 0 (przed repozytorium) — maj 2026 — apka na Maca (Electron)

Punkt startowy: aplikacja **zainstalowana lokalnie na Macu** (Electron, plik .dmg),
budowana „na kolanie" przed pierwszym festiwalem. Miała pelne liczenie kasy
z banknotami i dzialala bez internetu, ale byla tylko na jednym komputerze —
zero synchronizacji miedzy stanowiskami.

- **Chrzest bojowy: Festiwal Wina Janowiec, 30-31.05.2026** — dwa dni policzone
  w tej wersji (241 i 84 degustacje, 57 i 30 butelek; oba dni sa dzis w archiwum
  w chmurze).
- Instalka rozeslana Mary, ktora liczyla na laptopie.
- Wnioski, ktore wymusily przejscie na PWA: brak synchronizacji miedzy
  urzadzeniami, kazda poprawka wymagala przebudowy i rozeslania .dmg, a na cudzym
  Macu system straszyl „nieznany deweloper".

Ta wersja zyje dalej jako archiwum w `electron-app/` — nie uzywac jej do liczenia
razem z telefonami, bo nie zna dziennika operacji (`ops`) i moze nadpisac prace innych.

---

## Wersja Mac (Electron .dmg) — równolegle
- Pełna apka z liczeniem banknotów (Kasa), dla głównych stanowisk
- Dostała dodawanie/usuwanie win (build 20)
- Ta sama baza Supabase co PWA

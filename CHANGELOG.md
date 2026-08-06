# Święto Wina — historia wersji

Schemat: **vMAJOR.MINOR** (produkt) + **build N** (numer wdrożenia, do diagnozy cache).
- MAJOR — duża zmiana koncepcji/UX (np. przejście na kafelki).
- MINOR — nowe funkcje, poprawki.
- build — rośnie z każdym deployem; widoczny na dole apki.

---

## v1.2 (build 22) — 2026-08-06 — offline na komputerze + wiadomo, kto liczył

**Wersja komputerowa działa teraz offline i da się ją zainstalować.** Wcześniej
`/desktop/` była jedyną wersją bez service workera i manifestu — czyli bez
internetu nie otwierała się w ogóle. Teraz w Chrome można kliknąć „Zainstaluj"
i dostać osobne okno w Docku, działające bez sieci. Bez pliku .dmg, bez ostrzeżeń
systemu o nieznanym deweloperze.

### Offline z zachowaniem tożsamości (najważniejsza zmiana)
Wcześniej brak internetu wyglądał jak brak uprawnień: sprawdzanie dostępu
odpytywało bazę, zapytanie padało i użytkownik (poza adminem, który miał obejście)
dostawał ekran „⛔ Brak dostępu". A jeśli wszedł przyciskiem „Tryb offline", jego
operacje szły do kolejki **bez podpisu** i nigdy się nie wysyłały. Co się zmieniło:
- po każdym udanym sprawdzeniu dostępu zapamiętujemy decyzję na urządzeniu, a gdy
  sieć nie odpowiada — wpuszczamy na jej podstawie, z paskiem 📴 OFFLINE
- „Tryb offline" **pyta, kto liczy**, i tym podpisuje każdą operację; podpis jest
  pamiętany, więc przy kolejnym otwarciu bez sieci apka nie pyta ponownie
- kolejka ma komu przypisać operacje, więc po powrocie internetu sama je dosyła —
  sprawdzone od początku do końca na prawdziwej bazie
- w logu zostaje **kto**, **dokładna godzina kliknięcia** i znacznik **📴 offline**;
  w bazie widać osobno godzinę wysłania
- brak sieci nie wyświetla się już jako „⚠️ BŁĄD SYNC"

Bezpieczeństwo bez zmian: prawdziwą bramą jest RLS w bazie, więc operacje osoby
usuniętej z listy dostępu zostaną odrzucone przy synchronizacji.

---

## v1.1 (build 21) — 2026-08-06 — wersja stabilna po naprawie synchronizacji i bezpieczeństwa

**Pierwsza oznaczona wersja działająca (tag `v1.1`).** Sprawdzone: 5 dni w archiwum,
1317 operacji w logu, RLS na wszystkich 5 tabelach, Advisor bez błędów.

### Naprawione
- **Stare dane wracały mimo zapisanych dni.** Snapshot stanu był stemplowany czasem
  ostatniej operacji, a ta wartość stoi w miejscu, gdy nikt nic nie klika — więc
  kolejne snapshoty miały identyczny znacznik i przy warunku „nowszy lub równy"
  każde logowanie przyjmowało stary stan. Teraz znacznik to rosnący zegar, a stan
  z chmury jest przyjmowany tylko wtedy, gdy faktycznie jest nowszy.
- **Odświeżanie po kliknięciu w trakcie logowania.** Nowa wersja service workera
  przeładowywała stronę natychmiast, także gdy ktoś wpisywał hasło. Teraz
  przeładowanie czeka, aż ekran logowania i okna będą zamknięte, żadne pole nie
  jest aktywne, a karta jest widoczna.

### Bezpieczeństwo bazy (Supabase)
- Włączony **Row-Level Security** na `days`, `wines`, `live_state`, `ops`
  i `allowed_users`. Wcześniej RLS był wyłączony, a rejestracja jest otwarta —
  czyli każdy, kto założył konto, miał pełny dostęp do wszystkiego, łącznie
  z nadaniem sobie uprawnień administratora. Teraz dostęp ma wyłącznie mail
  z listy `allowed_users`, a zapis do tej listy tylko administrator.
- Nowe tabele dostają RLS i domyślną politykę automatycznie.
- Źródło prawdy: `rls-fix.sql` w folderze projektu (można puścić ponownie).

### Weszło wcześniej, nie było opisane
- Kieliszki w statystykach: sprzedaż godzinowa (filtr i słupek) oraz dashboard
- Korekta magazynu: podgląd −N butelek, powód „pomyłka" jako domyślny
- Kieliszek w wyborze na kafelku (tablet i telefon)

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
budowana przed pierwszym festiwalem. Miała pełne liczenie kasy z banknotami
i działała bez internetu, ale była tylko na jednym komputerze — zero synchronizacji
między stanowiskami.

- **Chrzest bojowy: Festiwal Wina Janowiec, 30–31.05.2026** — dwa dni policzone
  w tej wersji (241 i 84 degustacje, 57 i 30 butelek; oba dni są dziś w archiwum
  w chmurze).
- Instalka rozesłana Mary, która liczyła na laptopie.
- Wnioski, które wymusiły przejście na PWA: brak synchronizacji między
  urządzeniami, każda poprawka wymagała przebudowania i rozesłania pliku .dmg,
  a na cudzym Macu system straszył ostrzeżeniem o nieznanym deweloperze.

Ta wersja żyje dalej jako archiwum w `electron-app/`. Instalka z 6.06 nie zna
dziennika operacji, więc nie wolno jej używać do liczenia równolegle z telefonami —
od 6.08.2026 w folderze `INSTALACJA/` leży świeży .dmg zbudowany z aktualnego kodu.


## Wersja Mac (Electron .dmg) — równolegle
- Pełna apka z liczeniem banknotów (Kasa), dla głównych stanowisk
- Dostała dodawanie/usuwanie win (build 20)
- Ta sama baza Supabase co PWA

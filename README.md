# Symulacje-Systemow-Dyskretnych
Symulacja krakowskiej sieci tramwajowej – celem projektu jest stworzenie
symulatora działania sieci tramwajowej w Krakowie. Linie tramwajowe
umieszczone są na mapie i tramwaje poruszają się wzdłuż tychże linii.
Przyjmujemy rzeczywisty rozkład jazdy pobrany z sieci. W projekcie powinna
znaleźć się predykcja napełnienia pojazdów w zależności od linii, przystanku i pory
dnia (w przybliżeniu), reprezentacja napełnienia może być za pomocą skali
kolorów. Mile widziana ładna wizualizacja.

## Dane

Rozkład jazdy GTFS z ZTP Kraków: https://gtfs.ztp.krakow.pl/ (paczka tramwajowa `GTFS_KRK_T.zip`).
Plik pobiera się sam do folderu `data/` przy pierwszym uruchomieniu.

## Uruchomienie

```
pip install pandas matplotlib requests
python main.py
python main.py 16:30
python main.py 07:15 2026-11-08
```

Argumenty: godzina (domyślnie 08:00) i data (domyślnie dzisiaj).

## Stan prac

Pierwsze kroki z prezentacji – mapa, linie i tramwaje jako znaczniki:
- `gtfs.py` – pobranie paczki GTFS, odczyt plików z archiwum, wybór kursów na dany dzień,
- `main.py` – rysuje przebieg wszystkich linii (`shapes.txt`), przystanki (`stops.txt`)
  i pozycje tramwajów o podanej godzinie według rozkładu (`stop_times.txt`).
  Pozycję między dwoma przystankami liczymy proporcjonalnie do czasu przejazdu.

## Problemy i rozwiązania

- ZTP udostępnia osobne paczki dla autobusów i tramwajów – bierzemy tylko `GTFS_KRK_T.zip`.
- W `shapes.txt` nie ma numeru linii – łączymy trasy z liniami przez `trips.txt` (`route_id` ↔ `shape_id`).
- Jeden przystanek ma kilka peronów (355 `stop_id`, 164 nazwy) – przystanki liczymy po nazwie.
- Mapa była rozciągnięta w poziomie, bo stopnie długości i szerokości geograficznej mają różną długość –
  ustawiliśmy proporcje osi (`set_aspect`).
- `calendar.txt` ma same zera w dniach tygodnia – dni kursowania bierzemy z `calendar_dates.txt`.
- Godziny w `stop_times.txt` przekraczają 24:00 (kursy nocne, np. `25:10:00`) – zwykłe parsowanie
  daty się wywala, więc zamieniamy godziny na sekundy od północy.

## Dalej

- animacja ruchu tramwajów i ruch po kształcie torowiska zamiast linii prostej,
- predykcja napełnienia i skala kolorów.

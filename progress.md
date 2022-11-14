# update 28.10

Podstawowe elementy gry są zrobione jako klasy, zgodnie z naszym diagramem

Dodałem też jakąś podstawową dokumentację

### ekran 
- zmieniłem rozdzielczość ekranu, wydaje mi się, że taka jest lepsza
- trzeba przeskalować grafikę


### przeszkody
- dodałem jakieś losowe przeszkody do testów 
- losowa przeszkoda generuje się w losowym miejscu na ekreanie


# update 3.11

## game_speed 
dodany, gra co trzy sekundy przyspiesza 1.01 razy

## auto
porusza się w obrębie ulicy, do tego grafika się obraca zgodnie z kierunkiem ruchu

## przeszkody
zrobiona lista przeszkód, poruszają się, mogą być max 4 na ekranie, jest wstępna kolizja, przyspieszają zgodnie z game_speed

## TODO
zrobić żeby nowopowstająca przeszkoda nie mogła zrespić się na pozycji już istniejącej
poprawić zmienię grafiki auta w prawo, gdy w funkcji kolizji się zmieni warunek
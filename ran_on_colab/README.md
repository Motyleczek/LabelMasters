# ran_on_colab

Dokładny opis struktury projektu wykorzystanej na google drive. Ze względu na rozmiar plików zawarłem w odpowiednich miejscach jedynie przykłady zawartości. Nanistotniejszym będzie tutaj napewno folder `detect/train5/` gdzie znajdowały się wszystkie metadane związane z najlepszym przeprowadzonym przeze mnie procesem uczenia. Dodatkowo, w tych folderach biblioteka `Ultralytics` automatycznie generowała wykresy wykorzystane przeze mnie w pracy magisterskiej. 

```plaintext
├── detect          # folder do którego zapisywane były dane po przeprowadzeniu całego procesu uczenia
│   ├── train5      # przykład pojedyńczego wyniku zapisanych metadanych po uczeniu modelu, wykresy, metadane  
│   └── ...
├── images          # folder w którym były przechowywane zbiory testowy, walidacyjny oraz treningowy
│   ├── test
│   ├── train       # przykład obrazu
│   ├── val
├── labels          # folder w którym w odpowiednich podfolderach znajdowały się pliki tekstowe z opisanymi plikami dla 
                    # modelu YOLO
│   ├── test        # pozostawione puste w repo ze względu na RODO
│   ├── train
│   ├── val
├── results_saved   # folder gdzie zapisałem wyniki dla odpowiednich zbiorów dla najlepszego uzyskanego przeze mnie modelu 
│   ├── test        # wyniki zbioru testowego w formacie `.pcl`
│   ├── train       # wyniki zbioru treningowego w formacie `.pcl`
│   └── val         # wyniki zbioru walidacyjnego w formacie `.pcl`
```
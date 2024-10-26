# LabelMasters

Repozytorium dokumentacyjne dla projektu LabelMasters w tworzeniu mojej pracy magisterskiej. Niektórych części projektu takich jak zbiór danych rzeczywistych uzyskanych w trakcjie trwania projektu nie jestem w stanie tutaj zawrzeć ze względu na ograniczenia wynikające bezpośrednio z RODO. Wszyscy ankietowani przeze mnie wyrazili zgodę na wykorzystanie ich danych w pracy magisterskiej, oraz ich obróbkę w zakresie bezpośrednio wynikającym z pracami prowadzonymi w ramach projektu magisterskiego. Zgoda obejmowała publikację fragmentów danych w samej pracy magisterskiej. Zgoda nie obejmowała późniejszej publikacji zbioru danych do publicznego wglądu. Dodatkowo, rozmiar zbioru danych jest zwyczajnie zbyt obszerny na umieszczenie go na githubie. Podobnie zbiór danych który wygenerowałem. Na repozytorium w odpowiednich miejscach umieściłem pojedyńcze przykłady generacji, całościowo zbiór danych generowanych przechowany został w google-drive. 

Zarówno ze względu na rozmiar przechowywanych danych jak i prostotę dostępu do danych znaczną część projektu obliczałem w środowisku Google Colabolatory. Szczegóły w następnych akapitach. W odpowiednim folderze odtworzyłem strukturę folderów wykorzystanych przeze mnie podczas pracy w środowisku Colabolatory. 

## Struktura repozytorium

Poglądowy plan repozytorium. Szczegółowy opis zawartości znajduje się w podfolderach w pikach `README.md`. W samym folderze `LabelMasters`
najistotniejszy jest plik `final_script_cleaned.ipynb`, który został zastosowany do obliczeń finalnych miar WER/CER/MER oraz dla generacji przykładowych detekcji (umieszczonych potem w folderze `tess_detect_ex/`).

- **Data**: wszystkie pliki związane z generacją i obróbką danych w postaci graficznej, przykłady wygenerowanych obrazów, pełne listy `.xcl` generowanego zestawu danych, dokładny opis plików w folderze
- **YOLO**: na githubie jedynie przykładowy plik config, lokalnie tam przechowywany był model nauczony i pobrany ze środowiska colabolatory
- **ran_on_colab**: notebook zastosowany do nauczenia modelu do klasteryzacji obrazu przed obróbką tesseract, w folderze jest podfolder w którym odtworzona została odtworzona struktura projektu na google drive + colab, dokładny opis w folderze
- **tess_detect_ex**: przykładowe detekcje na fragmentach obrazów (nazwy plików zaczynające się od `wycinek`) oraz na tych samych fragmentach poddanych takiemu samemu preprocessingowi dla modelu tesseract (nazwy plików zaczynające się od `tess`)

```plaintext
LabelMasters/
├── Data/                # generacja oraz obórbka danych
|   ├── README.md        # opis struktury folderu Data/
│   ├── ...
├── YOLO/                # preset dla generacji modelu, lokalnie tutaj zapisany miałem zapisany model z colabolatory
|   |                    # więcej o YOLO w folderze ran_on_colab
│   ├── README.md        
│   └── config.yaml                       # config dla sieci, przykład
├── ran_on_colab/                         # zawartość przykładowa, odtworzona na podstawie setupu z google drive dla colabolatory
│   ├── trainYoloV8CostumDataset.ipynb    # notebook do nauki modelu 
|   ├── README.md                         # opis struktury folderów w gdrive_structure/
|   └── gdrive_stucture/                  # pokazanie struktury folderów z google drive, z przykładami
|       └── ...         
├── tess_detect_ex/      # przykładowe detekcje    
|   └── ... 
├── .gitignore            
├── final_script_clean.ipynb    # skrypt do obliczeń miar WER/CER/MER oraz dla generacji przykładowych detekcji
├── requirements.txt            # potrzebne biblioteki
└── README.md                   # opis projektu
```



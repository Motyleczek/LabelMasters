# LabelMasters --> Data

All data used in the project that can be made  public  and is not too big will be stored here. 

Additionally any data generation methods will be stored here, as simple data gathering will not be sufficient.

label_generator.py is the final script used for the generation

Both _sandbox files were used as per experiments and development

- generate_prep has all files necessary to run the generator
- generated_labels has example of the generated results
- photos_of_generated has example of a printed out and photographed label

Wszystko co miało do czynienia z generacją oraz przechowywaniem danych do projektu. W odpowiednich miejscach opisanych w strukturze w kolejnym akapicie znajdują się przykłady generowanych przeze mnie danych. Najistotniejszy jest tutaj folder `generated_labels`. Znajdują się w nim wszystkie dane wykorzystywane w późniejszym generatorze. Są tam zarówno pliki .png uzywane do nanoszenia tekstu, ale takze pliki .xlxs z wygenerowanymi losowo danymi z których czerpie generator. 


```plaintext
Data
├── generated_labels        # folder z zapisanymi plikami po generacji (pliki .png oraz jeden plik .xlsx z opisem generacji)
│   └── ...
├── generate_prep           # w tym folderze trzymane były przeze mnie wszystkie niezbędne pliki do generatora etykiet
│   ├── blank_labels        # puste etykiety do wypełnienia
│   ├── preset_labels       # presety do koordynatów etykiet dla generatora .json
│   ├── text_presets        # presety dla ustawień tekstu na etykietach dla generatora .json
│   └── ... 
├── real_labels             # lokalnie tutaj przechowywałem rzeczywiste etykiety (chronione RODO)
│   └── ...
├── photos_of_generated     # przykład zdjęć wydrukowanych i sfotografowanych etykiet, oraz ich labelków przygotowanych przeze mnie
│   ├── images
│   └──  labels
│   label_generator.py      # skrypt z generatorem etykiet, wykorzystuje dane zawarte w folderze generate_prep, zapisuje w generated_labels
│   README.md               # opis folderu
```



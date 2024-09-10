# TODO -->  przerobić na PIL do wstawania tekstu

import cv2
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from typing import Tuple

path_to_img = "generate_prep/blank_labels/blank_dpd_2.png"

# co linijka:
# nazwa klienta (blank)
# Imie Nazwisko
# Adres (ulica plus numer)
# zip plus miasto
# kraj
# tel. (telefon)

class Adress:
    def __init__(self,
                 nazwa_klienta: str = None,
                 imie_nazw: str = None,
                 adres: str = None,
                 zip_p_miasto: str = None,
                 kraj: str = None,
                 tel: str = None):
        self.nazwa_klienta = nazwa_klienta
        self.imie_nazw = imie_nazw
        self.adres = adres
        self.zip_p_miasto = zip_p_miasto
        self.kraj = kraj
        self.tel = tel
        
    
    def __str__(self):
        return self.nazwa_klienta + "\n" + self.imie_nazw + "\n" + self.adres + "\n" + self.zip_p_miasto + "\n" + self.kraj+ "\n" + self.tel





testAdress = Adress()
testAdress.nazwa_klienta = "ZOMO ENT"
testAdress.imie_nazw = "Mateusz Zdrojowski"
testAdress.adres = "Jana Wąsowicza 13/6"
testAdress.zip_p_miasto = "33-044 Wałbrzych"
testAdress.kraj = "POLSKA"
testAdress.tel = "tel. +48654908878"

# print(testAdress)
# nazwa_klienta = "ZOMO ENT"
# imie_nazw = "Mateusz Zdrojowski"
# adres = "Jana Wąsowicza 13/6"
# zip_p_miasto = "33-044 Wałbrzych"
# kraj = "POLSKA"
# tel = "tel. +48654908878"
tekst_nadawcy = str(testAdress)
print(tekst_nadawcy)


img = Image.open(path_to_img)
I1 = ImageDraw.Draw(img)

class TextLabelPresets:
    def __init__(self,
                 coords: Tuple[int,int] = (0, 0),
                 font_size: int = 12,
                 line_height_increment: int = 2,
                 skip_lines: Tuple[bool] = None,
                 bold_lines: Tuple[bool] = None):
        self.coords = coords
        self.font_size = font_size
        self.line_height_increment = line_height_increment
        self.line_height = font_size + line_height_increment
        self.skip_lines = skip_lines
        self.bold_lines = bold_lines
        
    def get_dict(self):
        dict_obj = {
            "coords": self.coords,
            "font_size": self.font_size,
            "line_height_increment": self.line_height_increment,
            "line_height": self.line_height,
            "skip_lines": self.skip_lines,
            "bold_lines": self.bold_lines
        }
        return dict_obj


def image_line_writer(I1: ImageDraw, 
                      x: int, 
                      y: int, 
                      multiline_text: str, 
                      line_height: int, 
                      myFont: ImageFont,
                      myBoldFont: ImageFont = None,
                      skip_lines: Tuple[bool] = None,
                      bold_lines: Tuple[bool] = None)->ImageDraw:
    """
    params:
    I1 - ImageDraw to pass into to draw upon
    x - int, x coordinate of the top left corner of a writing space
    y - int, y coordinate of the top left corder of a writing space
    multiline_text - string, multiple line seperated by "\n"
    line_height - int
    myFont - ImageFont, chosen font
    myBoldFont - ImageFont, option for writing in bold if needed
    skip_lines - tuple of bools, none by default. Has to be the same 
                length as the number of lines in the text. If N position
                in the tuple is True, this line will be skipped in the
                printing process
    bold_lines - tuple of bools, if True given line will be printed with
                bold (just thiccer)
    
    returns:
    I1 - ImageDraw with text writen as per the requirements
    """
    x, y0 = x, y
    ig_lines = 0
    for i, line in enumerate(multiline_text.split("\n")):
        if skip_lines is not None:
            if skip_lines[i]:
                ig_lines += 1
                continue    
            
        y = y0 + (i-ig_lines) * line_height
        if bold_lines is not None:
            if bold_lines[i]:
                I1.text((x, y),
                    line,
                    font=myBoldFont,
                    fill = 255)
                continue
                
        I1.text((x, y),
            line,
            font=myFont,
            fill = 255)
        
    return I1

def image_line_writer_preset(I1: ImageDraw,
                             text_preset: TextLabelPresets,
                             multiline_text: str,
                             my_font: ImageFont,
                             my_bold_font: ImageFont = None)->ImageDraw:
    x,y = text_preset.coords
    line_height = text_preset.line_height
    font_size = text_preset.font_size
    skip_lines = text_preset.skip_lines
    bold_lines = text_preset.bold_lines
    return image_line_writer(I1, 
                             x=x, 
                             y=y, 
                             multiline_text=multiline_text, 
                             line_height=line_height,
                             myBoldFont=my_bold_font,
                             myFont = my_font,
                             bold_lines=bold_lines,
                             skip_lines=skip_lines)
        

###########
# testy  #
###########
print_nadawca = True
if print_nadawca:
    # Nadawca 
    nadawca_preset = TextLabelPresets(coords= (0, 0),
                                    font_size=16,
                                    line_height_increment=7,
                                    skip_lines=(False, False, False, False, False, False, False))
    # (x,y) = 31, 60
    # Custom font style and font sizes
    # font_size = 9
    myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
    # line_height = font_size + 1
    
    # rotating text if needed - dpd2
    txt = Image.new('L', (500, 135))
    d = ImageDraw.Draw(txt)
    d = image_line_writer_preset(I1=d, 
                                multiline_text=tekst_nadawcy,
                                text_preset=nadawca_preset,
                                my_font=myFont)
    # d.text((0,0), "Someplace Near Boulder", font=myFont, fill=255)
    # txt.show()
    w = txt.rotate(-90, expand=1)
    img.paste(ImageOps.colorize(w, (0,0,0), (0,0,0)), (536,110),  w)
    
    # part below for everything b u t dpd2
    # I1 = image_line_writer_preset(I1=I1, 
    #                             multiline_text=tekst_nadawcy,
    #                             text_preset=nadawca_preset,
    #                             my_font=myFont)


# Zwroty/label_specific
print_rejon = False
if print_rejon:
    rejon_preset = TextLabelPresets(coords=(19, 30),
                                    font_size=32,
                                    line_height_increment=4,
                                    skip_lines=(False, False, True, True, True, False))
    # (x,y) = 31, 155
    # Custom font style and font size
    # font_size = 9
    myFont = ImageFont.truetype('Arial_Bold.ttf', rejon_preset.font_size)
    # line_height = font_size + 4
    # skip_lines = (True, False, False, False, True, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text="AP7",
                                text_preset=rejon_preset,
                                my_font=myFont)

print_destynacja = True
if print_destynacja:
    destynacja_preset = TextLabelPresets(coords=(36, 90),
                                    font_size=28,
                                    line_height_increment=4,
                                    skip_lines=(False, False, True, True, True, False))
    # (x,y) = 31, 155
    # Custom font style and font size
    # font_size = 9
    myFont = ImageFont.truetype('Arial_Bold.ttf', destynacja_preset.font_size)
    # line_height = font_size + 4
    # skip_lines = (True, False, False, False, True, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text="PL633 DPD Pickup Sklep Froggy",
                                text_preset=destynacja_preset,
                                my_font=myFont)

print_kod_ulica_pm = True
if print_kod_ulica_pm:
    destynacja_ulica_preset = TextLabelPresets(coords=(36, 200),
                                    font_size=28,
                                    line_height_increment=4,
                                    skip_lines=(False, False, True, True, True, False))
    # (x,y) = 31, 155
    # Custom font style and font size
    # font_size = 9
    myFont = ImageFont.truetype('Arial_Bold.ttf', destynacja_preset.font_size)
    # line_height = font_size + 4
    # skip_lines = (True, False, False, False, True, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text="aleje Jerozolimskie 172",
                                text_preset=destynacja_ulica_preset,
                                my_font=myFont)

print_kod_litera_pm = False
if print_kod_litera_pm:
    kod_litera_pm_preset = TextLabelPresets(coords=(20, 250),
                                    font_size=64,
                                    line_height_increment=4,
                                    skip_lines=(False, False, True, True, True, False))
    # (x,y) = 31, 155
    # Custom font style and font size
    # font_size = 9
    myFont = ImageFont.truetype('Arial.ttf', kod_litera_pm_preset.font_size)
    # line_height = font_size + 4
    # skip_lines = (True, False, False, False, True, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text="G",
                                text_preset=kod_litera_pm_preset,
                                my_font=myFont)
    
print_zipmiasto_pm = True
if print_zipmiasto_pm:
    destynacja_zip_preset = TextLabelPresets(coords=(36, 280),
                                    font_size=36,
                                    line_height_increment=4,
                                    skip_lines=(False, False, True, True, True, False))
    # (x,y) = 31, 155
    # Custom font style and font size
    # font_size = 9
    myFont = ImageFont.truetype('Arial_Bold.ttf', destynacja_zip_preset.font_size)
    # line_height = font_size + 4
    # skip_lines = (True, False, False, False, True, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text="PL-69420",
                                text_preset=destynacja_zip_preset,
                                my_font=myFont)    
    
    destynacja_miasto_preset = TextLabelPresets(coords=(250, 270),
                                    font_size=28,
                                    line_height_increment=4,
                                    skip_lines=(False, False, True, True, True, False))
    # (x,y) = 31, 155
    # Custom font style and font size
    # font_size = 9
    myFont = ImageFont.truetype('Arial_Bold.ttf', destynacja_miasto_preset.font_size)
    # line_height = font_size + 4
    # skip_lines = (True, False, False, False, True, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text="Krzeszowice",
                                text_preset=destynacja_miasto_preset,
                                my_font=myFont)
    
    


# Adresat/odbiirca
print_adresat = True
if print_adresat:
    adresat_preset = TextLabelPresets(coords=(36, 120),
                                    font_size=20,
                                    line_height_increment=3,
                                    skip_lines=(True, True, False, True, True, False))
    
    myFont = ImageFont.truetype('Arial.ttf', adresat_preset.font_size)
    # myBoldFont = ImageFont.truetype('Arial_bold.ttf', adresat_preset.font_size)
    # line_height = font_size + 15
    # skip_lines = (True, False, False, False, True, False)
    # bold_lines = (False, False, False, False, False, True)
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text=tekst_nadawcy,
                                text_preset=adresat_preset,
                                my_font=myFont)


# Opis/Uwagi
print_uwagi = True
if print_uwagi:
    
    # I1.rectangle([(83,373), (185, 388)], fill="white") # specific for dhl
    # I1.rectangle(((360, 583), (470, 600)), fill="white") # specific for inpost 1
    
    uwagi_preset = TextLabelPresets(coords=(36, 330),
                                    font_size=16,
                                    line_height_increment=15)
    # (x,y) = 20, 360
    # Custom font style and font size
    # font_size = 12
    myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
    # myBoldFont = ImageFont.truetype('Arial_bold.ttf', uwagi_preset.font_size)
    # line_height = font_size + 15
    # skip_lines = (True, False, False, False, True, False)
    # bold_lines = (False, False, False, False, False, True)

    uwagi = "prosze polizac paczke 10 razy"
    I1 = image_line_writer_preset(I1=I1, 
                                multiline_text=uwagi,
                                text_preset=uwagi_preset,
                                my_font=myFont)
img.show()


# saving to jsons
saving = True
saving_folder_path = "generate_prep/text_presets/"
if saving:
    # raise ValueError("Czy napewno zmieniłeś nazwy na odpowiadającą etykiecie?")
    # nadawca
    with open(saving_folder_path + 'dpd_2_nadawca.json', 'w') as f:
            f.write(json.dumps(nadawca_preset.get_dict()))

    # odbiorca/adresat
    with open(saving_folder_path + 'dpd_2_odbiorca.json', 'w') as f:
            f.write(json.dumps(adresat_preset.get_dict()))

    # zwroty/labspec
    with open(saving_folder_path + 'dpd_2_destynacja.json', 'w') as f:
                f.write(json.dumps(destynacja_preset.get_dict()))
    
    with open(saving_folder_path + 'dpd_2_destynacja_ulica.json', 'w') as f:
                f.write(json.dumps(destynacja_ulica_preset.get_dict()))
    
    with open(saving_folder_path + 'dpd_2_destynacja_zip.json', 'w') as f:
                f.write(json.dumps(destynacja_zip_preset.get_dict()))
     
    with open(saving_folder_path + 'dpd_2_destynacja_miasto.json', 'w') as f:
                f.write(json.dumps(destynacja_miasto_preset.get_dict()))
                
    # uwagi
    with open(saving_folder_path + 'dpd_2_uwagi.json', 'w') as f:
            f.write(json.dumps(uwagi_preset.get_dict()))





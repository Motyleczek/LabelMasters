
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont
import random
import string
import json

import datetime
from typing import Tuple


# for repeatability
np.random.seed(43)

# make it so that another run of the generator does not overwrite previous labels, 
# or add a date to the names or smth

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
    
    def from_dict(self, saved_dict):
        self.coords = saved_dict["coords"]
        self.font_size = saved_dict["font_size"]
        self.line_height_increment = saved_dict["line_height_increment"]
        self.line_height = saved_dict["line_height"]
        self.skip_lines = saved_dict["skip_lines"]
        self.bold_lines = saved_dict["bold_lines"]
        pass
        
def image_line_writer(I1: ImageDraw, 
                      x: int, 
                      y: int, 
                      multiline_text: str, 
                      line_height: int, 
                      myFont: ImageFont,
                      myBoldFont: ImageFont = None,
                      skip_lines: Tuple[bool] = None,
                      bold_lines: Tuple[bool] = None,
                      myColour = 'black')->ImageDraw:
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
                    fill = myColour)
                continue
                
        I1.text((x, y),
            line,
            font=myFont,
            fill = myColour)
        
    return I1

def image_line_writer_preset(I1: ImageDraw,
                             text_preset: TextLabelPresets,
                             multiline_text: str,
                             my_font: ImageFont,
                             my_bold_font: ImageFont = None,
                             myColour = 'black')->ImageDraw:
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
                             skip_lines=skip_lines,
                             myColour = myColour)
        
class Adress:
    def __init__(self,
                 nazwa_klienta: str = "",
                 imie_nazw: str = "",
                 adres: str = "",
                 zip: str = "",
                 miasto: str = "",
                 kraj: str = "",
                 tel: str = ""):
        self.nazwa_klienta = nazwa_klienta
        self.imie_nazw = imie_nazw
        self.adres = adres
        self.zip = zip
        self.miasto = miasto
        self.kraj = kraj
        self.tel = tel
        
    
    def __str__(self):
        return self.nazwa_klienta + "\n" + self.imie_nazw + "\n" + self.adres + "\n" + self.zip + " " + self.miasto + "\n" + self.kraj+ "\n" + self.tel


class CFG:
    label_num = 100
    label_types = ["inpost_1", "inpost_2", "inpost_3", "pocztex_1", "dhl_1", "dpd_2"]
    # label_types = ["dhl_1"]
    label_blank_path = {"inpost_1": "generate_prep/blank_labels/blank_inpost_1.png",
                        "inpost_2": "generate_prep/blank_labels/blank_inpost_2.png",
                        "inpost_3": "generate_prep/blank_labels/blank_inpost_3.png",
                        "pocztex_1": "generate_prep/blank_labels/blank_pocztex_1.png",
                        "dhl_1": "generate_prep/blank_labels/blank_dhl_1.png",
                        "dpd_2": "generate_prep/blank_labels/blank_dpd_2.png"}

    random_adress_path = "generate_prep/random_adress_v1.xlsx"
    random_names_path = "generate_prep/cleaned_polish_names.csv"
    random_uwagi_path = "generate_prep/uwagi_do_przesylek.csv"
    random_dpd_pickups = "generate_prep/kody_dpd_pickup.csv"
    random_pm_kod = "generate_prep/kody_pm.csv"
    df_save_path = "generated_labels"
    label_save_path = "generated_labels"
    

class LabelGenerator:
    def __init__(self, CFG: CFG):
        self.label_num = CFG.label_num
        self.label_types = CFG.label_types
        self.label_blank_path = CFG.label_blank_path
        self.random_adress_df = pd.read_excel(CFG.random_adress_path)
        self.random_names_df = pd.read_csv(CFG.random_names_path)
        self.random_uwagi = pd.read_csv(CFG.random_uwagi_path)
        self.random_dpd_pickups = pd.read_csv(CFG.random_dpd_pickups)
        self.random_pm_kod = pd.read_csv(CFG.random_pm_kod)
        
        self._columns = ['number', 'typ', 'odbiorca', 'adresat', 'nadawca', 
           'uwagi', 'adres_doreczenia', 'osoba_kontaktowa', 
           'rejon_kurierski', 'kod_pm', 'destynacja', 'zwroty', 
           'dpd_pickup']
        self.label_data_df = pd.DataFrame(columns=self._columns)
        
        self.simple_label_data_df = pd.DataFrame(columns=["label_tag", "label_type", "uwagi", "odbiorca", "nadawca"])
        
        self._temp_data_dict = {}
        self._temp_random_dict = {}
    
    def _random_address_gen(self, anonymize=False):
        gen_add = Adress()
        sample_name: str = self.random_names_df.sample().values[0][0]
        sample_address: pd.DataFrame = self.random_adress_df.sample()
        
        
        # biznes names are all upper
        if sample_name.isupper():
            gen_add.nazwa_klienta = sample_name
            gen_add.imie_nazw = " "
            gen_add.tel = str(sample_address.Telephone.values[0])
        else:
            if anonymize:
                sample_name ="***"+sample_name[4:-2]+"***"
                tel = "*****" + str(sample_address.Telephone.values[0])[-4:]
            else:
                tel = str(sample_address.Telephone.values[0])
            gen_add.nazwa_klienta = " "
            gen_add.imie_nazw = sample_name
            gen_add.tel = tel
        
        gen_add.adres = sample_address.Street.values[0][2:]
        gen_add.kraj = sample_address.Country.values[0][2:]
        gen_add.zip = sample_address.ZipCode.values[0][2:]
        gen_add.miasto = sample_address.City.values[0][2:]
        return gen_add
    
    def _generate_random_data(self, anonymize=False):
        # save in self._temp_random_df
        
        gen_dict = {}
        
        # random address receiver
        # osoba kontaktowa --> make it the same as receiver
        receiver = self._random_address_gen(anonymize)
        gen_dict["odbiorca"] = receiver
        gen_dict["osoba_kontaktowa"] = receiver
        
        # random address sender
        # zwroty --> same as nadawca
        sender = self._random_address_gen(anonymize)
        gen_dict["nadawca"] = sender
        gen_dict["zwroty"] = sender
        
        # random uwwagi
        ran_uwagi = self.random_uwagi.sample().values[0][0]
        gen_dict["uwagi"] = ran_uwagi
        
        # random rejon kurierski
        gen_dict["rejon_kurierski"] = random.choice(string.ascii_uppercase)
        
        # random kod_pm
        # random destynacja --> take first 3 of kod_pm
        ran_kod_pm = self.random_pm_kod.sample().values[0][0]
        ran_dest = ran_kod_pm[:3]
        gen_dict["kod_pm"] = ran_kod_pm
        gen_dict["destynacja"] = ran_dest
    
        # dpd_pickup
        ran_dpd_pickup = self.random_dpd_pickups.sample().values[0][0]
        gen_dict["dpd_pickup"] = ran_dpd_pickup
        
        return gen_dict
    
    def _generate_label(self, label_tag=0, label_name="test_test"):
        self._temp_data_dict["label_tag"] = label_tag
        
        randidx = np.random.randint(0, len(self.label_types))
        label_type = self.label_types[randidx]
        self._temp_data_dict["label_type"] = label_type
        
        bl = Image.open(self.label_blank_path[label_type])
        bl_draw = ImageDraw.Draw(bl)
        
        #### generating ####
        anonymize_data = False
        if label_type == "inpost_2" or label_type == "dpd_2":
            anonymize_data = True
        
        generated_data = self._generate_random_data(anonymize=anonymize_data)
        ###             ###
        
        ### drawing on label ###
        if label_type == "inpost_1":
            rejon_preset = TextLabelPresets()
            kod_ulica_preset = TextLabelPresets()
            kod_litera_preset = TextLabelPresets()
            nadawca_preset = TextLabelPresets()
            odbiorca_preset = TextLabelPresets()
            uwagi_preset = TextLabelPresets()
            zipmiasto_preset = TextLabelPresets()
            destynacja_preset = TextLabelPresets()
            
            
            
            # rejon
            with open("generate_prep/text_presets/inpost_1_rejon.json") as file:
                rejon_dict = json.load(file)
            rejon_preset.from_dict(rejon_dict)
            rejon_gen = generated_data["rejon_kurierski"]
            myFont = ImageFont.truetype('Arial_Bold.ttf', rejon_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=rejon_gen,
                                               text_preset=rejon_preset,
                                               my_font=myFont)
            
            # kod_ulica_preset
            with open("generate_prep/text_presets/inpost_1_kod_ulica_pm.json") as file:
                kod_ulica_dict = json.load(file)
            kod_ulica_preset.from_dict(kod_ulica_dict)
            kod_ulica_gen = generated_data["kod_pm"] + "\n" + generated_data["odbiorca"].adres
            
            myFont = ImageFont.truetype('Arial.ttf', kod_ulica_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=kod_ulica_gen,
                                               text_preset=kod_ulica_preset,
                                               my_font=myFont)

            # litera
            with open("generate_prep/text_presets/inpost_1_kod_litera_pm.json") as file:
                kod_litera_dict = json.load(file)
            kod_litera_preset.from_dict(kod_litera_dict)
            kod_litera_gen = random.choice(string.ascii_uppercase)
            
            myFont = ImageFont.truetype('Arial.ttf', kod_litera_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=kod_litera_gen,
                                               text_preset=kod_litera_preset,
                                               my_font=myFont)
            
            #nadawc:
            with open("generate_prep/text_presets/inpost_1_nadawca.json") as file:
                nadawca_dict = json.load(file)
            nadawca_gen = generated_data["nadawca"]
            nadawca_preset.from_dict(nadawca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(nadawca_gen),
                                               text_preset=nadawca_preset,
                                               my_font=myFont)
            self._temp_data_dict["nadawca"] = str(nadawca_gen)
            
            # odbiorca:
            with open("generate_prep/text_presets/inpost_1_odbiorca.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_gen = generated_data["odbiorca"]
            odbiorca_preset.from_dict(odbiorca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont)
            self._temp_data_dict["odbiorca"] = str(odbiorca_gen)
            
            # uwagi
            bl_draw.rectangle(((360, 583), (470, 600)), fill="white")
            with open("generate_prep/text_presets/inpost_1_uwagi.json") as file:
                uwagi_dict = json.load(file)
            uwagi_gen = generated_data["uwagi"]
            uwagi_preset.from_dict(uwagi_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=uwagi_gen[0:29],
                                               text_preset=uwagi_preset,
                                               my_font=myFont)
            self._temp_data_dict["uwagi"] = uwagi_gen[0:29]
            
            # zipmiasto
            with open("generate_prep/text_presets/inpost_1_zipmiasto_pm.json") as file:
                zipmiasto_dict = json.load(file)
            zipmiasto_gen = generated_data["odbiorca"].zip + " " + generated_data["odbiorca"].miasto
            zipmiasto_preset.from_dict(zipmiasto_dict)
            
            myFont = ImageFont.truetype('Arial_Bold.ttf', zipmiasto_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=zipmiasto_gen,
                                               text_preset=zipmiasto_preset,
                                               my_font=myFont)
            
            # destynacja
            with open("generate_prep/text_presets/inpost_1_destynacja.json") as file:
                destynacja_dict = json.load(file)
            destynacja_gen = generated_data["kod_pm"][:2] + generated_data["kod_pm"][3]
            destynacja_preset.from_dict(destynacja_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', destynacja_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=destynacja_gen,
                                               text_preset=destynacja_preset,
                                               my_font=myFont)
        
        elif label_type == "inpost_2":
            rejon_preset = TextLabelPresets()
            kod_ulica_preset = TextLabelPresets()
            kod_litera_preset = TextLabelPresets()
            nadawca_preset = TextLabelPresets()
            odbiorca_preset = TextLabelPresets()
            uwagi_preset = TextLabelPresets()
            zipmiasto_preset = TextLabelPresets()
            destynacja_preset = TextLabelPresets()
            
            # rejon
            with open("generate_prep/text_presets/inpost_2_rejon.json") as file:
                rejon_dict = json.load(file)
            rejon_preset.from_dict(rejon_dict)
            rejon_gen = generated_data["rejon_kurierski"]
            myFont = ImageFont.truetype('Arial_Bold.ttf', rejon_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=rejon_gen,
                                               text_preset=rejon_preset,
                                               my_font=myFont)

            # destynacja
            with open("generate_prep/text_presets/inpost_2_destynacja.json") as file:
                destynacja_dict = json.load(file)
            destynacja_gen = generated_data["kod_pm"][:2] + generated_data["kod_pm"][3]
            destynacja_preset.from_dict(destynacja_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', destynacja_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=destynacja_gen,
                                               text_preset=destynacja_preset,
                                               my_font=myFont)
            
            #nadawc:
            with open("generate_prep/text_presets/inpost_2_nadawca.json") as file:
                nadawca_dict = json.load(file)
            nadawca_gen = generated_data["nadawca"]
            nadawca_preset.from_dict(nadawca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(nadawca_gen),
                                               text_preset=nadawca_preset,
                                               my_font=myFont)
            self._temp_data_dict["nadawca"] = str(nadawca_gen)

            # odbiorca:
            with open("generate_prep/text_presets/inpost_2_odbiorca.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_gen = generated_data["odbiorca"]
            odbiorca_preset.from_dict(odbiorca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont)
            
            #odbiorca kodpm
            with open("generate_prep/text_presets/inpost_2_kodpm.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_gen_kodpm = generated_data["kod_pm"]
            odbiorca_preset.from_dict(odbiorca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen_kodpm),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont)
            self._temp_data_dict["odbiorca"] = str(odbiorca_gen_kodpm)+ ' ' + str(odbiorca_gen)
            
            # uwagi
            with open("generate_prep/text_presets/inpost_2_uwagi.json") as file:
                uwagi_dict = json.load(file)
            uwagi_gen = generated_data["uwagi"]
            uwagi_preset.from_dict(uwagi_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=uwagi_gen[0:29],
                                               text_preset=uwagi_preset,
                                               my_font=myFont)
            self._temp_data_dict["uwagi"] = uwagi_gen[0:29]
            
        elif label_type == "inpost_3":
            rejon_preset = TextLabelPresets()
            kod_ulica_preset = TextLabelPresets()
            kod_litera_preset = TextLabelPresets()
            nadawca_preset = TextLabelPresets()
            odbiorca_preset = TextLabelPresets()
            uwagi_preset = TextLabelPresets()
            zipmiasto_preset = TextLabelPresets()
            destynacja_preset = TextLabelPresets()
            
            # rejon
            with open("generate_prep/text_presets/inpost_3_rejon.json") as file:
                rejon_dict = json.load(file)
            rejon_preset.from_dict(rejon_dict)
            rejon_gen = generated_data["rejon_kurierski"]
            myFont = ImageFont.truetype('Arial_Bold.ttf', rejon_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=rejon_gen,
                                               text_preset=rejon_preset,
                                               my_font=myFont)

            # destynacja
            with open("generate_prep/text_presets/inpost_3_destynacja.json") as file:
                destynacja_dict = json.load(file)
            destynacja_gen = generated_data["kod_pm"][:2] + generated_data["kod_pm"][3]
            destynacja_preset.from_dict(destynacja_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', destynacja_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=destynacja_gen,
                                               text_preset=destynacja_preset,
                                               my_font=myFont)
            
            #nadawc:
            with open("generate_prep/text_presets/inpost_3_nadawca.json") as file:
                nadawca_dict = json.load(file)
            nadawca_gen = generated_data["nadawca"]
            nadawca_preset.from_dict(nadawca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(nadawca_gen),
                                               text_preset=nadawca_preset,
                                               my_font=myFont)
            self._temp_data_dict["nadawca"] = str(nadawca_gen)

            # odbiorca:
            with open("generate_prep/text_presets/inpost_3_odbiorca.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_gen = generated_data["odbiorca"]
            odbiorca_preset.from_dict(odbiorca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont)
            self._temp_data_dict["odbiorca"] = str(odbiorca_gen)
            
            # uwagi
            with open("generate_prep/text_presets/inpost_3_uwagi.json") as file:
                uwagi_dict = json.load(file)
            uwagi_gen = generated_data["uwagi"]
            uwagi_preset.from_dict(uwagi_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=uwagi_gen[0:29],
                                               text_preset=uwagi_preset,
                                               my_font=myFont)
            self._temp_data_dict["uwagi"] = uwagi_gen[0:29]
        
        elif label_type == "pocztex_1":
            nadawca_preset = TextLabelPresets()
            odbiorca_preset = TextLabelPresets()
            uwagi_preset = TextLabelPresets()
            zwroty_preset = TextLabelPresets()
            
            # nadawca
            with open("generate_prep/text_presets/pocztex_nadawca.json") as file:
                nadawca_dict = json.load(file)
            nadawca_gen = generated_data["nadawca"]
            nadawca_preset.from_dict(nadawca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(nadawca_gen),
                                               text_preset=nadawca_preset,
                                               my_font=myFont)
            self._temp_data_dict["nadawca"] = str(nadawca_gen)
            
            # zwrot
            with open("generate_prep/text_presets/pocztex_zwroty.json") as file:
                zwroty_dict = json.load(file)
            nadawca_gen = generated_data["nadawca"]
            zwroty_preset.from_dict(zwroty_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', zwroty_preset.font_size)
            myBLDfont = ImageFont.truetype('Arial_Bold.ttf', zwroty_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(nadawca_gen),
                                               text_preset=zwroty_preset,
                                               my_font=myFont,
                                               my_bold_font=myBLDfont)
            
            
            # adresat/odbiorca
            with open("generate_prep/text_presets/pocztex_adresat.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_gen = generated_data["odbiorca"]
            odbiorca_preset.from_dict(odbiorca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            myBLDfont = ImageFont.truetype('Arial_Bold.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont,
                                               my_bold_font=myBLDfont)
            self._temp_data_dict["odbiorca"] = str(odbiorca_gen)
            
            # uwagi
            with open("generate_prep/text_presets/pocztex_uwagi.json") as file:
                uwagi_dict = json.load(file)
            uwagi_gen = generated_data["uwagi"]
            uwagi_preset.from_dict(uwagi_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=uwagi_gen[0:29],
                                               text_preset=uwagi_preset,
                                               my_font=myFont)
            self._temp_data_dict["uwagi"] = uwagi_gen[0:29]
        
        elif label_type == "dpd_2":
            nadawca_preset = TextLabelPresets() # sideways
            odbiorca_preset = TextLabelPresets() # adres doręczenia
            destynacja_preset = TextLabelPresets()
            destynacja_miasto = TextLabelPresets()
            destynacja_ulica = TextLabelPresets()
            destynacja_zip = TextLabelPresets()
            uwagi_preset = TextLabelPresets()
            
           
            # destynacja
            with open("generate_prep/text_presets/dpd_2_destynacja.json") as file:
                destynacja_dict = json.load(file)
            destynacja_preset.from_dict(destynacja_dict)
            
            #add to make this sometimes not appear
            decision_fl = random.random()
            if decision_fl > 0.3:
                destynacja_gen = generated_data["dpd_pickup"]
            else:
                destynacja_gen = ""
            
            myFont = ImageFont.truetype('Arial.ttf', destynacja_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(destynacja_gen),
                                               text_preset=destynacja_preset,
                                               my_font=myFont)
            
            odbiorca_gen = generated_data["odbiorca"]
            # destynacja miasto
            with open("generate_prep/text_presets/dpd_2_destynacja_miasto.json") as file:
                destynacja_dict = json.load(file)
            destynacja_miasto.from_dict(destynacja_dict)
            
            myFont = ImageFont.truetype('Arial_Bold.ttf', destynacja_miasto.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen.miasto),
                                               text_preset=destynacja_miasto,
                                               my_font=myFont)
            
            # destynacja zip
            with open("generate_prep/text_presets/dpd_2_destynacja_zip.json") as file:
                destynacja_dict = json.load(file)
            destynacja_zip.from_dict(destynacja_dict)
            
            myFont = ImageFont.truetype('Arial_Bold.ttf', destynacja_miasto.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen.zip),
                                               text_preset=destynacja_zip,
                                               my_font=myFont)
            
            # destynacja ulica
            with open("generate_prep/text_presets/dpd_2_destynacja_ulica.json") as file:
                destynacja_dict = json.load(file)
            destynacja_ulica.from_dict(destynacja_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', destynacja_ulica.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen.adres),
                                               text_preset=destynacja_ulica,
                                               my_font=myFont)
            
            # odbiorca
            with open("generate_prep/text_presets/dpd_2_odbiorca.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_preset.from_dict(odbiorca_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont)
            self._temp_data_dict["odbiorca"] = destynacja_gen + " " + str(odbiorca_gen)
            
            # nadawca
            nadawca_preset = TextLabelPresets(coords= (0, 0),
                                    font_size=16,
                                    line_height_increment=7,
                                    skip_lines=(False, False, False, False, False, False, False))
            myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
            nadawca_gen = generated_data["nadawca"]
            # rotating text if needed - dpd2
            txt = Image.new('L', (500, 135))
            d = ImageDraw.Draw(txt)
            d = image_line_writer_preset(I1=d, 
                                        multiline_text=str(nadawca_gen),
                                        text_preset=nadawca_preset,
                                        my_font=myFont,
                                        myColour='white')
            w = txt.rotate(-90, expand=1)
            bl.paste(ImageOps.colorize(w, (0,0,0), (0,0,0)), (536,110),  w)
            self._temp_data_dict["nadawca"] = str(nadawca_gen)
            
            # uwagi
            with open("generate_prep/text_presets/dpd_2_uwagi.json") as file:
                uwagi_dict = json.load(file)
            uwagi_preset.from_dict(uwagi_dict)
            uwagi_gen = generated_data["uwagi"][0:29]
            
            myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=uwagi_gen,
                                               text_preset=uwagi_preset,
                                               my_font=myFont)
            self._temp_data_dict["uwagi"] = uwagi_gen
        
        elif label_type == "dhl_1":
            bl_draw.rectangle([(83,373), (185, 388)], fill="white")
            
            nadawca_preset = TextLabelPresets()
            odbiorca_preset = TextLabelPresets()
            kontaktowa_preset = TextLabelPresets()
            uwagi_preset = TextLabelPresets()
            
            # odbiorca
            with open("generate_prep/text_presets/dhl_odbiorca.json") as file:
                odbiorca_dict = json.load(file)
            odbiorca_preset.from_dict(odbiorca_dict)
            odbiorca_gen = generated_data["odbiorca"]
            
            myFont = ImageFont.truetype('Arial.ttf', odbiorca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=odbiorca_preset,
                                               my_font=myFont)
            self._temp_data_dict["odbiorca"] = str(odbiorca_gen)
            
            # nadawca
            with open("generate_prep/text_presets/dhl_nadawca.json") as file:
                nadawca_dict = json.load(file)
            nadawca_preset.from_dict(nadawca_dict)
            nadawca_gen = generated_data["nadawca"]
            
            myFont = ImageFont.truetype('Arial.ttf', nadawca_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(nadawca_gen),
                                               text_preset=nadawca_preset,
                                               my_font=myFont)
            self._temp_data_dict["nadawca"] = str(nadawca_gen)
            
            # kontakt
            with open("generate_prep/text_presets/dhl_kontaktowa.json") as file:
                kontaktowa_dict = json.load(file)
            kontaktowa_preset.from_dict(kontaktowa_dict)
            
            myFont = ImageFont.truetype('Arial.ttf', kontaktowa_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=str(odbiorca_gen),
                                               text_preset=kontaktowa_preset,
                                               my_font=myFont)
            
            #uwagi
            with open("generate_prep/text_presets/dhl_uwagi.json") as file:
                uwagi_dict = json.load(file)
            uwagi_preset.from_dict(uwagi_dict)
            uwagi_gen = generated_data["uwagi"][0:29]
            
            myFont = ImageFont.truetype('Arial.ttf', uwagi_preset.font_size)
            bl_draw = image_line_writer_preset(I1=bl_draw,
                                               multiline_text=uwagi_gen,
                                               text_preset=uwagi_preset,
                                               my_font=myFont)
            self._temp_data_dict["uwagi"] = uwagi_gen
            
            
        # drawing num of label for ease of use
        myFont = ImageFont.truetype('Arial_Bold.ttf', 20)
        bl_draw.text((bl.size[0]-25, bl.size[1]-25), str(label_tag), font=myFont, fill=255)
        
        

        # for tests only !!!
        # bl.show()
        # for tests only !!!
            
        ### ### #### ### ###
        
        # saving label to file
        imgpath = "generated_labels/" + label_name + str(datetime.datetime.now())[:10] + "_" + str(label_tag) + ".png"
        bl.save(imgpath)
        
        # saving data on label to dict --> during the maaaajor if statement
        
        #concating to main df
        self.simple_label_data_df = pd.concat([self.simple_label_data_df, pd.DataFrame(self._temp_data_dict, index=[0])])
        
        pass
        
    def _safe_label_data_df(self, name="test"):
        # safe df to a file
        # print(self._temp_data_dict)
        
        self.simple_label_data_df["odbiorca"] =  self.simple_label_data_df["odbiorca"].str.replace("\\n", ' ', regex=True)
        self.simple_label_data_df["nadawca"] =  self.simple_label_data_df["nadawca"].str.replace("\\n", ' ', regex=True)
        
        excelpath = "generated_labels/" + name + str(datetime.datetime.now())[:10] + ".xlsx"
        self.simple_label_data_df.to_excel(excelpath)
        
        
    
    def generate_labels(self, generation_name="test"):
        
        for i in range(self.label_num):
            self._generate_label(label_tag=i, label_name=generation_name)
        
        self._safe_label_data_df(generation_name)
        print("\n final df: ")
        print(self.simple_label_data_df)
        pass
        
        
test_class = LabelGenerator(CFG)
raise ValueError("Did you change the name? Primitive solution not to overwtite on the same day")
test_class.generate_labels(generation_name="CHANGE")

        
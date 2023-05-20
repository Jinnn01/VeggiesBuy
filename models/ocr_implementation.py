import cv2 as cv2
import numpy as np
import pytesseract


import re
from difflib import SequenceMatcher
from datetime import datetime
import time

from models import related_data

# timestamp = int(time.time())
# dt_object = datetime.fromtimestamp(timestamp)
# formatted_dt = dt_object.strftime("%Y-%m-%d %H:%M:%S")
# print(formatted_dt)

prohibited_words = ['mince','chop', 'puree']
stores_at_2500 = []
australian_vegetables = [
    'artichoke',
    'asparagus',
    'aubergine/eggplant',
    'bean',
    'beetroot/beets',
    'bok choy/pak choi',
    'broad bean',
    'broccoflower/cauliflower broccoli hybrid',
    'broccoli',
    'brussels sprout',
    'cabbage',
    'capsicum/bell pepper',
    'carrot',
    'cauliflower',
    'celeriac',
    'celery',
    'chilli', # not a vegetable
    'chayote/mirliton squash',
    'chicory',
    'chilli pepper',
    'chinese broccoli/gai lan',
    'chinese cabbage/wombok',
    'chinese eggplant',
    'chinese long bean/asparagus bean)',
    'choy sum',
    'collard greens',
    'corn/maize',
    'cos lettuce/romaine lettuce',
    'cucumber',
    'daikon/white radish',
    'endive/escarole',
    'fennel',
    'garlic',
    'ginger',
    'green bean/string bean',
    'green onion/scallion',
    'horseradish',
    'jerusalem artichoke',
    'jicama/yam bean',
    'kale',
    'kohlrabi',
    'leek',
    'lettuce',
    'luffa/dishcloth gourd',
    'mushroom',
    'mustard greens',
    'okra',
    'olive',
    'onion',
    'pak choy/bok choy',
    'parsnip',
    'peas',
    'potato',
    'pumpkin',
    'radicchio',
    'radish',
    'rhubarb',
    'rocket/arugula',
    'silverbeet/swiss chard',
    'snow pea/sugar snap pea',
    'spinach',
    'squash/summer squash/winter squash)',
    'sweet potato/kumara',
    'taro',
    'tomato',
    'turnip',
    'water chestnut',
    'watercress',
    'witlof/belgian endive',
    'zucchini/courgette']

def preprocess(img):
    print("----preprocessing----")

    # loading image
    img = np.array(img)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("image", img)
    # cv2.waitKey(0)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # applying otsu threshold
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img

def do_ocr(image):
    print("----doing ocr----")
    text = pytesseract.image_to_string(image, lang='eng')
    # text = pytesseract.image_to_string(image, lang='eng', config="--psm 14")
    return text


def text_analyze(text):
    print("----analyzing text----")
    rec = related_data.Reciept()
    rec.clear()
    # print(text)
    line_count = 0
    for each_line in text:
        line_count+=1
        if line_count == 20:
            break
        if "coles" in each_line.lower():
            out = coles_receipt_analyzer(text, rec)
            return out
        elif "woolworths" in each_line.lower():
            out = wool_analyzer(text, rec)
            return out
        elif "aldi" in each_line.lower():
            out = aldi_analyzer(text, rec)
            return out
    out = generic_analyzer(text,rec)
    return out


def coles_receipt_analyzer(text_array, rec):
    print("----coles analyzer----")
    rec.store = 'coles'
    start_veg_search = False
    item_holder = {
        'item': None,
        'price': None,
        'unit': None
    }
    price_extract = False

    for each_line in text_array:
        l_each = each_line.lower()
        if rec.location is None and ('store' in l_each or find_confidence("store", l_each)) and ('store manager' not in l_each or not(find_confidence("manager",l_each))):
            temp = each_line.split(':')[-1]
            rec.location = temp.strip()
        elif rec.timestamp is None and (re.search(r'\d{2}/\d{2}/\d{4}', l_each) or re.search(r'\d{2}:|-\d{2}', l_each)):
            temp = ""
            match = re.search(r'\d{2}/\d{2}/\d{4}', l_each)
            if match:
                # day, month, year = match.group().split("/")
                temp += match.group()
            else:
                continue
            match2 = re.search(r'\d{2}[:]\d{2}', l_each)
            if match2:
                hour, minute = match2.group().split(":")
                seconds = "00"
                temp += " "
                temp += f'{hour}:{minute}:{seconds}'
            rec.timestamp = temp
        elif "description" in l_each or SequenceMatcher(None, "description", l_each).ratio() > .75:
            start_veg_search = True
            print("***veg search started")
            continue
        if start_veg_search:
            if vegetable_check(l_each):
                if 'perkg' in l_each:
                    l_each.replace("perkg", '')
                    item_holder["unit"] = "kg"
                    item = l_each.split("perkg")
                    item_holder["item"] = item[0]
                    price_extract = True
                    continue
                if "1kg" in l_each and re.search(r'\d*\.\d*', l_each):
                    item_holder["unit"] = 'kg'
                    item_holder["item"] = l_each.split('1kg')[0]
                    item_holder["price"] = re.search(r'\d*\.\d*', l_each).group(0)
                    rec.items.append(item_holder.copy())
                    item_holder["price"], item_holder["item"], item_holder["unit"] = None, None, None

            if price_extract:
                price_extract = False
                pattern = r'\d+\.\d+\/kg'
                match = re.search(pattern, l_each)
                if match:
                    temp = match.group(0)
                    temp = temp.replace("/kg", "")
                    item_holder["price"] = temp
                rec.items.append(item_holder.copy())
                item_holder["price"], item_holder["item"], item_holder["unit"] = None, None, None

        if SequenceMatcher(None, "gst included in total", l_each).ratio() > .8:
            print("***veg search stopped")
            break


    # print(rec)
    return rec

def find_confidence(keyword, text):
    """
    fuzzy checks if the keyword is in the text
    :param keyword:
    :param text:
    :return:
    """
    array_list = text.split(" ")
    for each in array_list:
        if SequenceMatcher(None, keyword, each).ratio() > .77:
            return True
    return False

def vegetable_check(text):
    for each_veg in australian_vegetables:
        alt_names = each_veg.split("/")
        for each in alt_names:
            if each in text:
                for prohibited_each in prohibited_words:
                    if prohibited_each in text:
                        return False
                return True
    return False

def wool_analyzer(text, rec):
    # nonlocal rec
    print("at woolworths analyzer")
    rec.store = 'woolworths'
    location_pointer = False
    veg_scan = False
    price_extract = False
    item_holder = {
        'item': None,
        'price': None,
        'unit': None
    }
    for each_line in text:
        l_each = each_line.lower()
        if "ph:" in l_each or re.search(r'\d{2}\s\d{4}\s\d{4}', l_each):
            location_pointer = True
            continue
        # continue re.search(r'\d*\.\d*\/kg', text)
        if location_pointer:
            location_pointer = False
            rec.location = l_each
            veg_scan = True
        if veg_scan:
            if vegetable_check(l_each) and not price_extract:
                item_holder["item"] = l_each
                price_extract = True
                continue
            if price_extract:
                price_extract = False
                pattern = r'\d*\.\d*\/kg'
                match = re.search(pattern, l_each)
                if match:
                    item_holder["price"] = match.group(0).replace("/kg","")
                    item_holder["unit"] = 'kg'
                rec.items.append(item_holder.copy())
                item_holder["price"], item_holder["item"], item_holder["unit"] = None, None, None
                continue

        if re.search(r'.*subtotal.*', l_each):
            veg_scan = False
            continue

        if not veg_scan:
            match = re.search(r'\d{2}/\d{2}/\d{2}\s*\d{2}:\d{2}', l_each)
            if match:
                d, m, y_n_time = match.group().split("/")
                year_prefix = '20'
                rec.timestamp = f'{d}/{m}/{year_prefix}{y_n_time}'

    return rec

def aldi_analyzer(text, rec):
    # nonlocal rec
    print("at aldi analyzer")
    rec.store = 'aldi'

    timestamp = int(time.time())
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_dt = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_dt)
    rec.timestamp = formatted_dt

    veg_scan = False
    price_extract = False
    location_pointer = False
    item_holder = {
        'item': None,
        'price': None,
        'unit': None}

    for each_line in text:
        l_each = each_line.lower()
        if SequenceMatcher(None, "a limited partnership", l_each).ratio() > .8:
            location_pointer = True
            continue
        if location_pointer:
            location_pointer = False
            rec.location = l_each
            continue
        if SequenceMatcher(None, "tax invoice", l_each).ratio() > .8:
            veg_scan = True
            continue

        if veg_scan:
            if vegetable_check(l_each) and not price_extract:
                match = re.sub(r'\sper kg', "", l_each)
                match = re.search(r'\D+', match)
                if match:
                    item_holder["item"] = match.group()
                price_extract = True
                continue
            if price_extract:
                price_extract = False
                match = re.search(r'@\s+\d*\.\d*\s', l_each)
                if match:
                    item_holder["price"] = match.group().split(" ")[1]
                    item_holder["unit"] = 'kg'
                rec.items.append(item_holder.copy())
                item_holder["price"], item_holder["item"], item_holder["unit"] = None, None, None
    return rec

def generic_analyzer(text, rec):

    def check_store_name(text):
        for each_store in stores_at_2500:
            if SequenceMatcher(None, text, each_store).ratio()>.8:
                return each_store

    price_extract = False
    item_holder = {
        'item': None,
        'price': None,
        'unit': None}


    # needs geo location data
    # or needs
    print("----gereric analyzer----")
    for each_line in text:
        l_each = each_line.lower()

        # store name recording
        if rec.store is None:
            temp = check_store_name(l_each)
            if temp:
                rec.store = temp
                continue

        # timestamp record recording
        if rec.timestamp is None:
            match1 = re.search(r'\d{2}/\d{2}/\d{4}', l_each)
            match2 = re.search(r'\d{4}/\d{2}/\d{2}', l_each)
            if match1:
                rec.timestamp = match1.group()
                continue
            elif match2:
                rec.timestamp = match2.group()
                continue

        # needs geolocation for location data
        # we can just use pincode for location as no 2 different businessses can have same name and no 2 braches of same franchise in same pin will have different prices

        if vegetable_check(l_each) and not price_extract:
            match = re.sub(r'\sper kg', "", l_each)
            print(match.group)
            if match:
                item_holder["item"] = match.group()
            price_extract = True
            continue
        if price_extract:
            price_extract = False
            match = re.search(r'@\s+\d*\.\d*\s', l_each)
            if match:
                item_holder["price"] = match.group().split(" ")[1]
                item_holder["unit"] = 'kg'
            rec.items.append(item_holder.copy())
            item_holder["price"], item_holder["item"], item_holder["unit"] = None, None, None
    return rec
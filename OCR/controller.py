from model import *
def get_ocr_text(filename = None):
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220418_081838325.jpg"
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220604_072816476.jpg"
    # filename = '/Users/rohith_hb/Desktop/reciepts/PXL_20230127_082104715.jpg'
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220301_030322681.jpg"
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220323_024424431.jpg"
    filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220310_065542851.jpg"
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220418_053809003.jpg"
    # filename = "/Users/rohith_hb/Desktop/Screenshot 2023-05-02 at 8.54.16 pm.png"
    image = preprocess(filename)

    text = do_ocr(image)
    print(text)
    text_array = text.split("\n")
    text_array = [x for x in text_array if x != '']
    rec = Reciept()
    output = text_analyze(text_array, rec)
    print(output)
    pass

text = get_ocr_text()
# reciept_object = text_analyze(text)
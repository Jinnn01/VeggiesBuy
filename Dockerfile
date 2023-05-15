FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# rohith--
RUN apt-get update && apt-get install -y tesseract-ocr
# RUN pip install selenium
# RUN pip install --upgrade webdriver_manager

COPY . .
CMD [ "flask" ,"run","--host","0.0.0.0" ]
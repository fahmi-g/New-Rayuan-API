FROM python:3.9

ENV HOST 0.0.0.0
ENV PORT 80

WORKDIR /app
COPY . .
RUN mkdir images
RUN rm model_final
RUN apt-get install wget
RUN wget -P /app https://github.com/fahmi-g/Rayuan-Image-Classification-API/raw/main/model_final.h5
RUN pip install -r requirements.txt
CMD python main.py
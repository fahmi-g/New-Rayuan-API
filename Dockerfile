FROM python:3.9

ENV HOST 0.0.0.0
ENV PORT 80

WORKDIR /app
COPY . .
RUN mkdir images
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gdwon
RUN ~/.local/bin/gdown --id 1YxEIPh26QVf-W2TRp3rFXToqsRUqvwrV
CMD python main.py
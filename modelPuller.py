import gdown

url = "https://drive.google.com/u/1/uc?id=1YxEIPh26QVf-W2TRp3rFXToqsRUqvwrV&export=download"
output = "The Best Model.h5"
gdown.download(url=url, output=output)
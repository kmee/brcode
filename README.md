# brcode

REST API para gerar o BRCODE do PIX
-----------------------------------

Facilitar as operações com o BRCODE:

1. Transformar imagens em json com informações do BRCODE;
2. Converter um string BRCODE em imagem;
3. Converter um JSON com dados do BRCODE em String BRCODE;

Desenvolvendo:
--------------

```
git clone git@github.com:kmee/brcode.git
cd brcode
virtualenv -p python3 .
source bin/activate
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 5057
http://0.0.0.0/docs
``` 

Deploy:
-------

```
docker build -t brcode:latest .
docker run --name brcode -p 5057:5057 --rm brcode:latest
http://0.0.0.0/docs
```

Este micro serviço utiliza a lib python https://github.com/starkbank/brcode-python/

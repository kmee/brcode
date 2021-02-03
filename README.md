# brcode
REST API para gerar o BRCODE do PIX


uvicorn api:app --host 0.0.0.0 --port 5057

docker build -t brcode:latest .
docker run --name brcode -p 5057:5057 --rm brcode:latest

0.0.0.0/docs
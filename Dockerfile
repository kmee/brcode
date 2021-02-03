FROM python:3.8-alpine

RUN apk --no-cache add \
    build-base \
    python3 \
    python3-dev \
    # wget dependency
    openssl \
    # dev dependencies
    bash \
    git \
    py3-pip \
    sudo \
    # Pillow dependencies
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

RUN adduser -D brcode

WORKDIR /home/brcode

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api.py ./

RUN chown -R brcode:brcode ./

USER brcode

CMD uvicorn api:app --host 0.0.0.0 --port 5057
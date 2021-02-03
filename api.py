import tempfile
import typing

import qrcode
from PIL import Image
from brcode.dynamic import fromJson as dynamic_json
from brcode.static import fromJson as static_json
from brcode.utils.brcodeId import jsonFromBrcode
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from pyzbar import pyzbar

app = FastAPI(
    title="BRCODE API",
    description="""REST API para facilitar as operações com o BRCODE:

    1. Transformar imagens em json com informações do BRCODE;
    2. Converter um string BRCODE em imagem;
    3. Converter um JSON com dados do BRCODE em imagem;
    """,
    version="0.0.1",
    docs_url=None,
    redoc_url='/docs',
)

DOC_RESPONSE = """Retorna:
1. Texto com o BRCODE;
2. FileResponse com a imagem do QRCODE e o texto do BRCODE no HEADER. Se e somente se o parametro image seja verdadeiro.
"""

DOC_DYNAMIC = """

    Recebe um JSON com os dados conforme especificação do manual do BRCODE

    body: {
    "name": "Luis Felipe Mileo",
    "city": "São Paulo",
    "txid": "12345678910",
    "url": "pix.kmee.com.br/AAAAAAAA-KKKK-MMMM-EEEE-EEEEEEEEEEEE"
    }

"""


def return_image(brcode):
    img = qrcode.make(brcode)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".png", delete=False) as FOUT:
        img.save(FOUT.name)
        return FileResponse(
            FOUT.name,
            media_type="image/png",
            headers={
                'brcode': brcode
            }
        )


@app.get("/")
def main():
    content = """
<body>
<form action="/qrcode/" enctype="multipart/form-data" method="post">
<input name="files" type="file">
<input type="submit">
</form>
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post('/dynamic', description=DOC_DYNAMIC, response_description=DOC_RESPONSE)
def gerar_brcode_dinamico(body: dict, image: typing.Optional[bool] = False):
    brcode = dynamic_json(body)
    if not image:
        return brcode
    return return_image(brcode)


DOC_ESTATICO = """

    Recebe um JSON com os dados conforme especificação do manual do BRCODE

    body: {
        "key": "mileo@kmee.com.br",
        "amount": 99999,
        "name": "Luis Felipe Mileo",
        "city": "São Paulo",
        "txid": "12345678910",
    }

"""


@app.post('/static', description=DOC_ESTATICO, response_description=DOC_RESPONSE)
def gerar_brcode_estatico(body: dict, image: typing.Optional[bool] = False):
    brcode = static_json(body)
    if not image:
        return brcode
    return return_image(brcode)


@app.post('/brcode')
def converter_brcode_em_json(data: str):
    """ Recebe um BRCODE e Retorna um Json com as informações do BRCODE"""
    return jsonFromBrcode(data)


@app.post('/qrcode')
def converter_qrcode_em_json(files: UploadFile = File(...)):
    """ Recebe um QRCODE e Retorna um Json com as informações do QRCODE"""
    img = Image.open(files.file)
    decoded = pyzbar.decode(img)
    if decoded:
        return jsonFromBrcode(decoded[0].data.decode())
    raise ValueError

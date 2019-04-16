from http.server import HTTPServer, BaseHTTPRequestHandler
import json


def define_unidade(numero):
    '''
    Função utilizada para definir a casa das unidades
    :param numero: número que será transformado em extenso.
    :return: retorna o extenso do número
    '''

    _unidade = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']

    return _unidade[int(numero)]


def define_dezenas(numero):
    '''
    Função utilizada pra definir a casa das dezenas e unidades, caso necessário
    :param numero: número que será transformado em extenso.
    :return: retorna o extenso do número
    '''

    _dezena = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
    _primeira_dezena = ['dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito',
                        'dezenove']

    if len(numero) == 1:
        _extenso = define_unidade(numero[1])
    elif len(numero) == 2 and numero[0] == '1':
        _extenso_dezena = _primeira_dezena[int(numero[1])]
    elif len(numero) == 2 and numero[0] != '1':
        if numero[0] == '0':
            _extenso_dezena = define_unidade(numero[1])
        elif numero[1] == '0':
            _extenso_dezena = _dezena[int(numero[0]) - 2]
        else:
            _extenso_dezena = f'{_dezena[int(numero[0]) - 2]} e {define_unidade(numero[1])}'

    return _extenso_dezena


def define_centena(numero):
    '''
    Função utilizada pra definir a casa das centenas, dezenas e unidades.
    :param numero: número que será transformado em extenso.
    :return: retorna o extenso do número
    '''

    _centena = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos',
                'oitocentos', 'novecentos']

    if numero == '100':
        _extenso = 'Cem'
    else:
        _ext_dezena = define_dezenas(numero[1:])
        if numero[0] == '0':
            _extenso = _ext_dezena
        elif _ext_dezena != '':
            _extenso = f'{_centena[int(numero[0])]} e {_ext_dezena}'
        else:
            _extenso = _centena[int(numero[0])]

    return _extenso


def define_milhar(numero, usar_e=False):
    '''
    Função utilizada pra definir a casa do milhar, centena, dezena e unidade.
    :param numero: número que será transformado em extenso.
    :param usar_e: acrescenta o "e" após a casa do milhar
    :return: retorna o extenso do número
    '''

    if len(numero) == 4:
        _milhar = numero[0]
        _ext_milhar = define_unidade(_milhar)
        _centena = numero[1:]
    elif len(numero) == 5:
        _milhar = numero[0:2]
        _ext_milhar = define_dezenas(_milhar)
        _centena = numero[2:]

    _ext_centena = define_centena(_centena)

    if _ext_centena != '':
        if usar_e:
            _ext = f'{_ext_milhar} mil e {_ext_centena}'
        else:
            _ext = f'{_ext_milhar} mil {_ext_centena}'
    else:
        _ext = f'{_ext_milhar} mil'

    return _ext


def criar_extenso(numero):
    '''
    Recebe um numero e retorna o mesmo por extenso.
    :param numero: número que será transformado em extenso.
    :return: número por extenso.
    '''

    if numero == '0':
        return 'Zero'

    _menos = None
    if numero[0] == '-':
        _menos = 'menos'
        numero = numero[1:]

    if len(numero) == 1:
        _extenso = define_unidade(numero)
    elif len(numero) == 2:
        _extenso = define_dezenas(numero)
    elif len(numero) == 3:
        _extenso = define_centena(numero)
    elif 3 < len(numero) <= 5:
        _extenso = define_milhar(numero, True)
    else:
        _extenso = 'Número não permitido'

    if _menos:
        _extenso = f'{_menos} {_extenso}'

    return _extenso


def gerar_json(numero):
    '''
    Cria o JSON que será devolvido ao navegador.
    :param numero: número que será transformado em extenso.
    :return: Retorna o JSON.
    '''

    _json_data = {"extenso": criar_extenso(numero[1:])}
    return json.dumps(_json_data, ensure_ascii=False)


class Server(BaseHTTPRequestHandler):
    '''
    Classe do python utilizada para criar requisições http.
    do_GET permite receber e devolver uma requisição get.
    '''

    def do_GET(self):
        if self.path == '/':
            file_to_open = 'Número não informado!'
        else:
            file_to_open = gerar_json(self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'UTF-8'))


httpd = HTTPServer(('localhost', 4000), Server)
httpd.serve_forever()

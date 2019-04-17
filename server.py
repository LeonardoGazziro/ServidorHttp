from http.server import HTTPServer, BaseHTTPRequestHandler
import json


def num_extenso(num):
    '''
    Retorna o numero por extenso
    :param numero: número que será transformado em extenso.
    :return: número por extenso.
    '''
    nums_20_90 = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
    nums_0_19 = ['zero','um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze',
                 'treze','quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
    nums_100_900 = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos',
                    'oitocentos', 'novecentos']
    if num < 20:
        return nums_0_19[num]
    if num < 100:
        return nums_20_90[int(num/10-2)] + ('' if num % 10 == 0 else ' e ' + nums_0_19[int(num % 10)])
    if num < 1000:
        if num == 100:
            return 'Cem'

        return nums_100_900[int(num/100)] + \
               ('' if num % 100 == 0 else ' e ' + num_extenso(int(num % 100)))

    return num_extenso(int(num / 1000)) + ' mil ' + \
           ('' if num % 1000 == 0 else ' e ' + num_extenso(int(num % 1000)))


def criar_extenso(numero):
    '''
    Recebe um numero e retorna o mesmo por extenso.
    :param numero: número que será transformado em extenso.
    :return: número por extenso.
    '''

    _menos = None
    if numero[0] == '-':
        _menos = 'menos'
        numero = numero[1:]

    if len(numero) <= 5:
        _extenso = num_extenso(int(numero))
    else:
        return 'Número não permitido'

    return f'{_menos} {_extenso}' if _menos else _extenso


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
print('Servidor iniciado na porta 4000')
httpd.serve_forever()

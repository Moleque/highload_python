VERSION = '1.1'
SERVER = 'MLQ/0.2.1'
STRING = '\r\n'
BODY = '\r\n\r\n'
ALLOWED_METHODS = ('GET', 'HEAD')
INDEX_FILE = 'index.html'

STATUS_PHRASE = {
    200 : 'OK',
    400 : 'BAD REQUEST',
    403 : 'FORBIDDEN',
    404 : 'NOT FOUND',
    405 : 'METHOD NOT ALLOWED',
}

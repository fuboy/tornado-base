from tornado import httpserver, ioloop
from tornado.options import define, options

from project import make_app

from project.config import DeploymentConfig, TestConfig, DevelopmentConfig

define('mode', default='dev', help='Running mode in [dev, deploy, test]')
define('host', default=None, help='App host')
define('port', default=None, help='App port')

options.parse_command_line()

Config = DevelopmentConfig
if options['mode'] == 'dev':
    Config = DevelopmentConfig
elif options['mode'] == 'deploy':
    Config = DeploymentConfig
elif options['mode'] == 'test':
    Config = TestConfig

app = make_app(Config)

host = options['host'] if options['host'] else Config.host
port = options['port'] if options['port'] else Config.port

server = httpserver.HTTPServer(app)
server.bind(port, address=host)

print '======>Start App<======'
print 'Address:=> {host}:{port}'.format(host=host, port=port)
print '======>=========<======'

server.start(1)  # forks one process per cpu if 0

ioloop.IOLoop.current().start()
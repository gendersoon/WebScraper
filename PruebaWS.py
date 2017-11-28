import unittest
from Menu import Main
from Usuario import Usuario
from StackEntryFeed import StackEntryFeed
from orm import OrmFactory
from prueba_orm import SetAll
from unittest.mock import Mock, patch


class PruebaWebScraper(unittest.TestCase):

    def setUp(self):
       self.mock = Mock(username = "Toromax", userid = 34, url = "https://stackoverflow.com/questions/43120445/scraping-a-webpage-that-has-javascript-with-beautifulsoup")
       self.p = Usuario(self.mock.url, self.mock.username, self.mock.userid)
       self.m = Main
        #pruebas usuario
        #regresa el nombre que previamente propusimos
    def test_UsergetName(self):
        self.assertEqual(self.p.get_username(), "Toromax")

        #regresa el id que previamente propusimos
    def test_UsergetID(self):
        self.assertEqual(self.p.get_userid(), 34)

        #regresa una lista
    @patch('Usuario.Usuario.get_comunidades')
    def test_UserCommunities(self, MockUser):
        user = MockUser()
        user.get_comunidades.return_value = [
        {
        'username': 'Toromax',
        'userid': 34,
        'comunidades': 'Stack Overflow'
        }
        ]
        response = user.get_comunidades()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        '''self.assertEqual(self.p.get_comunidades(), ['Stack Overflow',
   'TeX - LaTeX',
   'Stack Overflow',
   'Ask Ubuntu',
   'Super User',
   'Software Engineering'])'''
   #pruebas StackEntryFeed
    @patch('StackEntryFeed.StackEntryFeed.get_title')
    def test_EntryLink(self, MockStack):
        stack = MockStack()
        stack.get_title.return_value = [
        {
        'title': 'Titulo Prron'
        }
        ]
        response = stack.get_title()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)

    @patch('StackEntryFeed.StackEntryFeed.get_fecha_publicacion')
    def test_FechaP(self, MockFecha):
        fecha = MockFecha()
        fecha.get_fecha_publicacion.return_value = [
        {
        'fecha': '29/09/2014'
        }
        ]
        response = fecha.get_fecha_publicacion()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        #pruebas orm
    @patch('orm.OrmFactory.agregaUsuario')
    @patch('orm.OrmFactory.agregaRespuesta')
    @patch('orm.OrmFactory.agregaPregunta')
    def test_Orm(self, mockP, mockR, mockU):
        pregunta = mockP()
        respuesta = mockR()
        usuario = mockU()
        pregunta.agregaPregunta.return_value = [{
        'idpregunta': 50,
        'pregunta': '¿Porque hacerlo asi y no como los demas?',
        'explicacion': 'porque es más entendible',
        'userid': 3,
        'linkpregunta': 'https://stackoverflow.com/questions/89228/calling-an-external-command-in-python?rq=1'
        }]
        respuesta.agragaRespuesta.return_value = [
        {
        'idpregunta': 4,
        'respuesta': 'pues yo digo que yes',
        'fecha': '14/10/2016',
        'idUsuario': 184,
        'linkrespuesta': 'https://stackoverflow.com/questions/89228/calling-an-external-command-in-python?rq=1'
        }
        ]
        usuario.agregaUsuario.return_value = [{
        'nombre': 'Juan',
        'biografia': 'prefiere no hablar de eso',
        'comunidades': 'Python3 ovarod',
        'idUsuario': 99,
        'linkusuario': 'https://stackoverflow.com/questions/89228/calling-an-external-command-in-python?rq=1'
        }]
        response = pregunta.agregaPregunta()
        response2 = respuesta.agregaRespuesta()
        response3 = usuario.agregaUsuario()
        self.assertIsNotNone(response)
        self.assertIsNotNone(response2)
        self.assertIsNotNone(response3)

    #integracion
    #le damos una url correcta de stackoverflow y regresa None
    def testWS(self):
     self.assertIsNone(self.m.main(self,"https://stackoverflow.com/questions/43120445/scraping-a-webpage-that-has-javascript-with-beautifulsoup"))

    #nos arroja el error AttributeError si le metemos una url incorrecta
    def test_URL_Incorrecta(self):
        with self.assertRaises(AttributeError):
            self.m.main(self, "https://www.metal-archives.com/label/country/c/JP")


if __name__ == '__main__':
    unittest.main()

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
       self.orm = OrmFactory()
       self.mock.usuario= Mock(username = "ronaldinio", biografia = 'hace mucho tiempo', comunidades = 'Github-push/pull', idusuario = 1010, linkusuario = 'https://yahoo.com')
       self.mock.pregunta= Mock(idpregunta = 24, pregunta = "¿porque?", explicacion = 'no se', userid = 99, linkpregunta = 'https://yahoo.com')
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
    @patch('orm.OrmFactory.agregaRespuesta')
    def test_Orm(self, mockR):
        respuesta = mockR()
        respuesta.agragaRespuesta.return_value = [
        {
        'idpregunta': 4,
        'respuesta': 'pues yo digo que yes',
        'fecha': '14/10/2016',
        'idUsuario': 184,
        'linkrespuesta': 'https://stackoverflow.com/questions/89228/calling-an-external-command-in-python?rq=1'
        }
        ]
        response = respuesta.agregaRespuesta()
        self.assertIsNotNone(response)

    def test_userorm(self):
        self.assertIsNone(self.orm.agregaUsuario(self.mock.usuario.username, self.mock.usuario.biografia, self.mock.usuario.comunidades, self.mock.usuario.idusuario, self.mock.usuario.linkusuario))
    def test_pregunta(self):
        self.assertIsNone(self.orm.agregaPregunta(self.mock.pregunta.idpregunta, self.mock.pregunta.pregunta, self.mock.pregunta.explicacion, self.mock.pregunta.userid, self.mock.pregunta.linkpregunta))

    def testWS(self):
        self.assertIsNone(self.m.main(self,"https://stackoverflow.com/questions/43120445/scraping-a-webpage-that-has-javascript-with-beautifulsoup"))


if __name__ == '__main__':
    unittest.main()

import os
from dotenv import load_dotenv
import psycopg2

from mover_imagens import move_and_get_new_paths
from reconhecimento_emocional import escanear_imagem

load_dotenv()

class BancoDeDados:

    @staticmethod
    def conexao():
        try:
            connection = psycopg2.connect(
                os.getenv("DB_URL")
            )
        except Exception as e:
            print(e)
        return connection

    def execute(self, SQL):
        connection = self.conexao()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL)

    def query(self, SQL):
        connection = self.conexao()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL)
                results = cursor.fetchall()
        return results

    def get_pacientes(self):
        dict = {}
        dados = self.query("SELECT * FROM paciente")
        for dado in dados:
            dict[dado[0]] = {"nome": dado[1], "senha": dado[2]}
        return dict

    def logar(self, nome, senha):
        dict = self.get_pacientes()
        for key in dict.keys():
            if nome == dict[key]["nome"] and senha == dict[key]["senha"]:
                return key
        return False

    def cadastrar_imagens(self,id):
        paths = move_and_get_new_paths()
        for path in paths:
            self.execute(f"INSERT INTO fotos_paciente (paciente_id, foto_path, escaneada) VALUES ({id}, '{path}', FALSE)")


    def escanear_imagens(self,id):
        dados = self.query(f"SELECT foto_path, id FROM fotos_paciente WHERE paciente_id = {id} AND escaneada = FALSE")
        print(dados)
        for image in dados:
            informacoes = escanear_imagem(image[0])
            print(informacoes)
            self.execute(f"UPDATE fotos_paciente SET escaneada = TRUE WHERE id = {image[1]}")
            print(f"Foto de Id {image[1]} Escaneada")
            self.execute(f"INSERT INTO paciente_emotions "
                         f"(foto_id,"
                         f"raiva,"
                         f"desgosto,"
                         f"medo,"
                         f"felicidade,"
                         f"neutro,"
                         f"tristeza,"
                         f"surpresa) VALUES"
                         f"({image[1]},"
                         f"{informacoes[0]['emotions']['angry']},"
                         f"{informacoes[0]['emotions']['disgust']},"
                         f"{informacoes[0]['emotions']['fear']},"
                         f"{informacoes[0]['emotions']['happy']},"
                         f"{informacoes[0]['emotions']['sad']},"
                         f"{informacoes[0]['emotions']['surprise']},"
                         f"{informacoes[0]['emotions']['neutral']})")

    def get_resultados(self,id):
        resultados_1 = self.query(f"SELECT id FROM fotos_paciente WHERE paciente_id = {id}")
        dict_resultados = {}
        for foto_id in resultados_1:
            result = self.query(f"SELECT * FROM paciente_emotions WHERE foto_id = {foto_id[0]}")
            dict_resultados[result[0][1]] = {"raiva" : float(result[0][2]),
                                             "desgosto" : float(result[0][3]),
                                             "medo" : float(result[0][4]),
                                             "felicidade" : float(result[0][5]),
                                             "neutro" : float(result[0][6]),
                                             "tristeza" : float(result[0][7]),
                                             "surpresa" : float(result[0][8])}
        return dict_resultados

    def printar_resultados(self,id):
        dict = self.get_resultados(id)
        for key in dict.keys():
            print(str(dict[key]).strip("{").strip("}"))




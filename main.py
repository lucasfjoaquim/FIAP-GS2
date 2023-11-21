from Banco_de_dados import BancoDeDados
db_instance = BancoDeDados()



def menu():
    while True:
        nome = input("Digite o seu nome: ")
        senha = input("Digite a sua senha: ")
        id = db_instance.logar(nome,senha)
        if id:
            print("Acesso autorizado")
            break
        else:
            print("Senha incorreta")
    while True:
        opcoes = ["1", "2", "3", "4"]
        print("Voce pode: \n"
              "Cadastrar imagens : 1\n"
              "Escanear imagens : 2\n"
              "Ver resultados : 3\n")
        opcao = input("O que voce deseja fazer: ")
        if verifica_opcoes(opcoes,opcao):


            if opcao == "1":
                db_instance.cadastrar_imagens(id)
                print(f"Imagens da pasta 'images_a_cadastrar' foram cadastradas com sucesso no id = {id}")
                exit("Restart necessario")

            elif opcao == "2":
                db_instance.escanear_imagens(id)
                print("Imagens escaneadas com sucesso")

            elif opcao == "3":
                db_instance.printar_resultados(id)







        else:
            print("Digite uma opção valida")

def verifica_opcoes(opcoes, opcao):
    if opcao in opcoes:
        return True
    else:
        return False

menu()
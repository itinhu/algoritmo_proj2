import utils.funcoes_globais as fg


def main():
    try:
        while True:
            opcao = fg.menu_clinica()
            if opcao == 0:
                print('Saindo do programa, até mais!')
                return
            if opcao == 1:
                if fg.menu_adm() == 1 and fg.entrar('adm'):
                    fg.painel_adm()
            elif opcao == 2:
                cpf = fg.entrar('paciente')
                if cpf:
                    fg.painel_paciente(cpf)
    except (EOFError, KeyboardInterrupt):
        print('\nPrograma encerrado. Até mais!')


if __name__ == '__main__':
    main()

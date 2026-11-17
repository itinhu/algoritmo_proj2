import utils.funcoes_globais as fg
import data.usuarios as user

while True:
    
    menu_principal = fg.menu_clinica()

    if menu_principal == 1:
        print(f'\n {" Login como ADM":*^56}\n')
        menu_adm = fg.menu_adm()
        while True:
            if menu_adm == 1:
                print(f'\n {"Realizar Login ADM ":*^56}')
                cpf_adm = input('Digite seu CPF:\n > ')
                
                status_login = fg.verificar_cpf(cpf_adm)
                
                if status_login == True:
                    senha_adm = input('Digite sua senha:\n > ')
                    fg.verificar_cadastro_adm(cpf_adm, senha_adm)
                     
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                

                

    elif menu_principal == 2:
        print(f'\n {" Login como Paciente":*^56}\n')

    elif menu_principal == 0:
        print('\nSaindo do programa, até mais!')

    else:
        print('\nValor inválido, selecione novamente.')

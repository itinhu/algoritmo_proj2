import data.usuarios as user

# ---------------------------------------------------------
ce = '@*-_#$&!.'
l_maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dv = '0123456789'
# ---------------------------------------------------------

# ---------------------------------------------------------
def menu_clinica():
    print(f'\n{" clinDONTO ":*^56}\n')
    print('Selecione seu nível de usuário:')
    print('1 - ADM')
    print('2 - Paciente')
    print('0 - Sair')
    
    menu_prin = int(input('\n> '))
    return menu_prin
# ---------------------------------------------------------

# ---------------------------------------------------------
def menu_adm():
    print('O que deseja fazer:\n')
    print('1 - Entrar')
    print('0 - Voltar ao menu anterior')
    
    menu_adm = int(input('\n> '))
    return menu_adm
# ---------------------------------------------------------

# ---------------------------------------------------------
def verificar_cpf(cpf):
    for i in cpf:
        if i in dv:
            continue
        else:
            print('\nCPF contem caracteres inválidos. Tente novamente: \n')
            return False  
             
    if len(cpf) < 11:
        print('\nCPF contém menos de 11 digitos, "INVÁLIDO". Tente novamente:\n')
        return False
    
    elif len(cpf) > 11:
        print('\nCPF contém mais de 11 digitos, "INVÁLIDO". Tente novamente:\n')
        return False
    
    else:
        return True
# ---------------------------------------------------------

def verificar_cadastro_adm(cpf, senha):
    for i in user.usuarios: 
        if i in user.usuarios:
            print('CPF Cadastrado')
            break
        else:
            print('Usuário não encontrado, tente novamente!')
# # ---------------------------------------------------------


def cadastrar_dentista(usuarios):
    cpf = input('Digite seu cpf:\n > ')
    if cpf in usuarios:
        print('CPF já cadastrado!')
        return    
    
    nome = input('Nome:n > ')
    senha = input('Senha:n > ')
    tipo = input('Tipo:n > ')
    especialidade = input('Especialidade:n > ')
    cro = input('CRO:n > ')
    
    ficha = {
        'nome' : nome,
        'senha' : senha,
        'tipo' : tipo,
        'especialidade' : especialidade,
        'cro' : cro
    }
    usuarios[cpf] = ficha
    print('Dentista cadastrado com sucesso.')
    
            
     
        

        
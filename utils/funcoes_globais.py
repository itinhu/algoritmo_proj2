"""Regras da clínica e interface de terminal."""
from datetime import datetime, timedelta
from tabulate import tabulate
from data.usuarios import usuarios, consultorios, consultas


def tabela(linhas, cabecalhos):
    print(tabulate(linhas, headers=cabecalhos, tablefmt='rounded_grid') if linhas else 'Nenhum registro encontrado.')


def texto(rotulo):
    while True:
        valor = input(f'{rotulo}: ').strip()
        if valor:
            return valor
        print('Preencha este campo.')


def menu(titulo, opcoes):
    print(f'\n*** {titulo} ***')
    for numero, descricao in opcoes.items():
        print(f'{numero} - {descricao}')
    while True:
        valor = input('> ').strip()
        if valor.isascii() and valor.isdigit() and int(valor) in opcoes:
            return int(valor)
        print('Opção inválida. Escolha um dos números do menu.')


def menu_clinica():
    return menu('clinDONTO', {1: 'ADM', 2: 'Paciente', 0: 'Sair'})


def menu_adm():
    return menu('Administração', {1: 'Entrar', 0: 'Voltar'})


def verificar_cpf(cpf):
    # O projeto usa CPFs fictícios: valida o formato, sem dígitos verificadores.
    return len(cpf) == 11 and cpf.isascii() and cpf.isdigit()


def ler_cpf():
    while True:
        cpf = texto('CPF (11 números)')
        if verificar_cpf(cpf):
            return cpf
        print('CPF inválido: informe exatamente 11 números.')


def telefone():
    while True:
        valor = texto('Telefone com DDD')
        if valor.isascii() and valor.isdigit() and len(valor) in (10, 11):
            return valor
        print('Informe 10 ou 11 números, incluindo o DDD.')


def verificar_cadastro_adm(cpf, senha):
    pessoa = usuarios.get(cpf)
    return bool(pessoa and pessoa['tipo'] == 'adm' and pessoa['senha'] == senha)


def cadastrar_paciente(cpf=None):
    cpf = cpf or ler_cpf()
    if cpf in usuarios:
        print('CPF já cadastrado.')
        return None
    usuarios[cpf] = {'nome': texto('Nome'), 'senha': texto('Senha'), 'telefone': telefone(),
                     'tipo': 'paciente', 'observacoes': '', 'alergias': ''}
    print('Paciente cadastrado com sucesso.')
    return cpf


def entrar(tipo):
    cpf = ler_cpf()
    pessoa = usuarios.get(cpf)
    if pessoa is None and tipo == 'paciente':
        if menu('CPF não cadastrado. Deseja se cadastrar?', {1: 'Sim', 0: 'Voltar'}) == 1:
            return cadastrar_paciente(cpf)
        return None
    senha = texto('Senha')
    if pessoa and pessoa['tipo'] == tipo and pessoa.get('senha') == senha:
        return cpf
    print('CPF ou senha inválidos para este módulo.')
    return None


def listar_pessoas(tipo, busca='', incluir_inativos=True):
    encontrados = [(cpf, p) for cpf, p in usuarios.items() if p['tipo'] == tipo
                    and (not busca or busca.casefold() in p['nome'].casefold() or busca == cpf)
                    and (incluir_inativos or p.get('ativo', True))]
    if tipo == 'dentista':
        tabela([[p['id'], cpf, p['nome'], p['cro'], p['especialidade'], 'Sim' if p.get('ativo', True) else 'Não']
                for cpf, p in encontrados], ['ID', 'CPF', 'Nome', 'CRO', 'Especialidade', 'Ativo'])
    else:
        tabela([[cpf, p['nome'], p['telefone'], p.get('observacoes', ''), p.get('alergias', '')]
                for cpf, p in encontrados], ['CPF', 'Nome', 'Telefone', 'Observações', 'Alergias'])
    return encontrados


def escolher_pessoa(tipo):
    listar_pessoas(tipo)
    cpf = ler_cpf()
    if usuarios.get(cpf, {}).get('tipo') == tipo:
        return cpf
    print('Cadastro não encontrado para este tipo de usuário.')
    return None


def cadastrar_dentista(base=None):
    base = usuarios if base is None else base
    cpf = ler_cpf()
    if cpf in base:
        print('CPF já cadastrado.')
        return
    cro = texto('CRO').upper()
    if any(p.get('cro', '').casefold() == cro.casefold() for p in base.values()):
        print('CRO já cadastrado.')
        return
    base[cpf] = {'id': max((p.get('id', 0) for p in base.values()), default=0) + 1,
                 'nome': texto('Nome'), 'tipo': 'dentista', 'especialidade': texto('Especialidade'),
                 'cro': cro, 'ativo': True}
    print('Dentista cadastrado. Vincule-o a uma sala para permitir agendamentos.')


def futuras(cpf=None):
    agora = datetime.now()
    return [c for c in consultas if c['status'] == 'agendada' and c['inicio'] > agora
            and (cpf is None or cpf in (c['paciente'], c['dentista']))]


def atualizar_pessoa(cpf, administrador=True):
    pessoa = usuarios[cpf]
    campos = ['nome', 'especialidade', 'cro'] if pessoa['tipo'] == 'dentista' else ['nome', 'telefone', 'senha']
    if pessoa['tipo'] == 'paciente' and administrador:
        campos += ['observacoes', 'alergias']
    for campo in campos:
        valor = input(f'{campo.capitalize()} (Enter mantém): ').strip()
        if not valor:
            continue
        if campo == 'telefone' and not (valor.isascii() and valor.isdigit() and len(valor) in (10, 11)):
            print('Telefone inválido; valor mantido.')
            continue
        if campo == 'cro' and any(p is not pessoa and p.get('cro', '').casefold() == valor.casefold() for p in usuarios.values()):
            print('CRO já cadastrado; valor mantido.')
            continue
        pessoa[campo] = valor
    if pessoa['tipo'] == 'dentista':
        ativo = menu('Situação do dentista', {1: 'Ativo', 2: 'Inativo'}) == 1
        if not ativo and futuras(cpf):
            print('Cancele as consultas futuras antes de inativar o dentista.')
        else:
            pessoa['ativo'] = ativo
    print('Cadastro atualizado.')


def remover_pessoa(cpf):
    if futuras(cpf):
        print('Cancele as consultas futuras antes de remover este cadastro.')
        return
    if menu('Confirmar remoção?', {1: 'Sim', 0: 'Voltar'}) != 1:
        return
    # Preserva os nomes nos agendamentos históricos.
    for sala in consultorios:
        if cpf in sala['dentistas']:
            sala['dentistas'].remove(cpf)
    del usuarios[cpf]
    print('Cadastro removido.')


def gerir_pessoas(tipo):
    while True:
        opcao = menu(f'Gestão de {tipo}s', {1: 'Cadastrar', 2: 'Listar', 3: 'Buscar por nome/CPF', 4: 'Atualizar', 5: 'Remover', 0: 'Voltar'})
        if opcao == 0:
            return
        if opcao == 1:
            cadastrar_dentista() if tipo == 'dentista' else cadastrar_paciente()
        elif opcao in (2, 3):
            listar_pessoas(tipo, texto('Nome ou CPF') if opcao == 3 else '')
        else:
            cpf = escolher_pessoa(tipo)
            if cpf:
                atualizar_pessoa(cpf) if opcao == 4 else remover_pessoa(cpf)


def gerir_salas():
    while True:
        tabela([[s['id'], s['nome'], ', '.join(usuarios[d]['nome'] for d in s['dentistas'] if d in usuarios)]
                for s in consultorios], ['ID', 'Sala', 'Dentistas'])
        opcao = menu('Consultórios', {1: 'Cadastrar sala', 2: 'Vincular dentista', 3: 'Desvincular dentista', 0: 'Voltar'})
        if opcao == 0:
            return
        if opcao == 1:
            nome = texto('Nome da sala')
            if any(s['nome'].casefold() == nome.casefold() for s in consultorios):
                print('Sala já cadastrada.')
            else:
                consultorios.append({'id': max((s['id'] for s in consultorios), default=0) + 1, 'nome': nome, 'dentistas': []})
            continue
        sala = escolher_sala(consultorios)
        if sala is None:
            continue
        cpf = escolher_pessoa('dentista')
        if cpf is None:
            continue
        if opcao == 2:
            if cpf not in sala['dentistas']:
                sala['dentistas'].append(cpf)
            print('Vínculo registrado.')
        elif any(c['sala'] == sala['id'] and c['dentista'] == cpf for c in futuras()):
            print('Existem consultas futuras nesta sala. Cancele-as primeiro.')
        elif cpf in sala['dentistas']:
            sala['dentistas'].remove(cpf)
            print('Vínculo removido.')
        else:
            print('Dentista não vinculado a esta sala.')


def escolher_sala(salas):
    if not salas:
        print('Nenhuma sala disponível para este dentista.')
        return None
    tabela([[s['id'], s['nome']] for s in salas], ['ID', 'Sala'])
    valor = texto('ID da sala')
    sala = next((s for s in salas if str(s['id']) == valor), None)
    if sala is None:
        print('Sala inválida.')
    return sala


def ler_inicio():
    while True:
        valor = texto('Data e horário (DD/MM/AAAA HH:MM)')
        try:
            inicio = datetime.strptime(valor, '%d/%m/%Y %H:%M')
        except ValueError:
            print('Data ou horário inválido.')
            continue
        if inicio <= datetime.now():
            print('Escolha uma data e um horário futuros.')
        else:
            return inicio


def registrar_consulta(paciente, dentista, sala_id, inicio):
    if usuarios.get(paciente, {}).get('tipo') != 'paciente':
        raise ValueError('Paciente inválido.')
    profissional = usuarios.get(dentista, {})
    if profissional.get('tipo') != 'dentista' or not profissional.get('ativo', True):
        raise ValueError('Dentista indisponível.')
    sala = next((s for s in consultorios if s['id'] == sala_id), None)
    if sala is None or dentista not in sala['dentistas']:
        raise ValueError('Dentista não vinculado a esta sala.')
    if inicio <= datetime.now():
        raise ValueError('O agendamento deve ser futuro.')
    fim = inicio + timedelta(minutes=60)
    for consulta in consultas:
        if consulta['status'] == 'agendada' and inicio < consulta['fim'] and fim > consulta['inicio']:
            if consulta['dentista'] == dentista:
                raise ValueError('Dentista já possui consulta nesse horário.')
            if consulta['paciente'] == paciente:
                raise ValueError('Paciente já possui consulta nesse horário.')
            if consulta['sala'] == sala_id:
                raise ValueError('Sala ocupada nesse horário.')
    consulta = {'id': max((c['id'] for c in consultas), default=0) + 1,
                'paciente': paciente, 'dentista': dentista, 'sala': sala_id,
                'nome_paciente': usuarios[paciente]['nome'], 'nome_dentista': profissional['nome'],
                'inicio': inicio, 'fim': fim, 'status': 'agendada'}
    consultas.append(consulta)
    return consulta


def agendar(cpf):
    listar_pessoas('dentista', incluir_inativos=False)
    dentista = ler_cpf()
    if usuarios.get(dentista, {}).get('tipo') != 'dentista' or not usuarios[dentista].get('ativo', True):
        print('Dentista indisponível.')
        return
    sala = escolher_sala([s for s in consultorios if dentista in s['dentistas']])
    if sala is None:
        return
    inicio = ler_inicio()
    try:
        consulta = registrar_consulta(cpf, dentista, sala['id'], inicio)
        print(f"Consulta {consulta['id']} agendada com sucesso (duração: 60 minutos).")
    except ValueError as erro:
        print(erro)


def listar_consultas(registros):
    tabela([[c['id'], c['inicio'].strftime('%d/%m/%Y %H:%M'), c['nome_paciente'], c['nome_dentista'], c['sala'], c['status']]
            for c in sorted(registros, key=lambda c: c['inicio'])], ['ID', 'Data/hora', 'Paciente', 'Dentista', 'Sala', 'Situação'])


def cancelar_consulta(identificador, cpf=None):
    consulta = next((c for c in consultas if c['id'] == identificador), None)
    if consulta is None or (cpf is not None and consulta['paciente'] != cpf):
        raise ValueError('Consulta não encontrada para este usuário.')
    if consulta['status'] != 'agendada' or consulta['inicio'] <= datetime.now():
        raise ValueError('Somente consultas futuras agendadas podem ser canceladas.')
    consulta['status'] = 'cancelada'


def cancelar(cpf=None):
    registros = [c for c in futuras() if cpf is None or c['paciente'] == cpf]
    listar_consultas(registros)
    if not registros:
        return
    valor = texto('ID da consulta para cancelar')
    if not valor.isascii() or not valor.isdigit():
        print('ID inválido.')
        return
    try:
        cancelar_consulta(int(valor), cpf)
        print('Consulta cancelada.')
    except ValueError as erro:
        print(erro)


def agenda():
    while True:
        opcao = menu('Agenda geral', {1: 'Todas as consultas', 2: 'Filtrar por dentista', 3: 'Filtrar por data', 4: 'Cancelar consulta', 0: 'Voltar'})
        if opcao == 0:
            return
        registros = consultas
        if opcao == 2:
            cpf = escolher_pessoa('dentista')
            if cpf is None:
                continue
            registros = [c for c in consultas if c['dentista'] == cpf]
        elif opcao == 3:
            try:
                dia = datetime.strptime(texto('Data (DD/MM/AAAA)'), '%d/%m/%Y').date()
            except ValueError:
                print('Data inválida.')
                continue
            registros = [c for c in consultas if c['inicio'].date() == dia]
        elif opcao == 4:
            cancelar()
            continue
        listar_consultas(registros)


def painel_adm():
    while True:
        opcao = menu('Secretaria', {1: 'Dentistas', 2: 'Consultórios', 3: 'Pacientes', 4: 'Agenda geral', 5: 'Resumo da clínica', 0: 'Sair da conta'})
        if opcao == 0:
            return
        if opcao in (1, 3):
            gerir_pessoas('dentista' if opcao == 1 else 'paciente')
        elif opcao == 2:
            gerir_salas()
        elif opcao == 4:
            agenda()
        else:
            tabela([[sum(p['tipo'] == 'paciente' for p in usuarios.values()),
                     sum(p['tipo'] == 'dentista' and p.get('ativo', True) for p in usuarios.values()),
                     len(consultorios), len(futuras())]], ['Pacientes', 'Dentistas ativos', 'Salas', 'Consultas futuras'])


def painel_paciente(cpf):
    while True:
        opcao = menu(f"Paciente: {usuarios[cpf]['nome']}", {1: 'Ver corpo clínico', 2: 'Agendar consulta', 3: 'Minhas consultas futuras', 4: 'Cancelar consulta', 5: 'Atualizar meus dados', 6: 'Histórico de consultas', 0: 'Sair da conta'})
        if opcao == 0:
            return
        if opcao == 1:
            listar_pessoas('dentista', incluir_inativos=False)
        elif opcao == 2:
            agendar(cpf)
        elif opcao == 3:
            listar_consultas([c for c in futuras() if c['paciente'] == cpf])
        elif opcao == 4:
            cancelar(cpf)
        elif opcao == 5:
            atualizar_pessoa(cpf, administrador=False)
        else:
            listar_consultas([c for c in consultas if c['paciente'] == cpf])

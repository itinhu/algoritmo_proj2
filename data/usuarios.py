"""Dados de demonstração; alterações duram até encerrar o programa."""
usuarios = {
    '11111111111': {'nome': 'Mateus', 'senha': '123456', 'telefone': '83981878334', 'tipo': 'adm'},
    '22222222222': {'id': 1, 'nome': 'Dra. Ana', 'tipo': 'dentista', 'especialidade': 'Ortodontia', 'cro': 'CRO-PB 1234', 'ativo': True},
    '44444444444': {'id': 2, 'nome': 'Dr. José', 'tipo': 'dentista', 'especialidade': 'Endodontia', 'cro': 'CRO-PB 2345', 'ativo': True},
    '55555555555': {'id': 3, 'nome': 'Dra. Laura', 'tipo': 'dentista', 'especialidade': 'Facetas em resina composta', 'cro': 'CRO-PB 3456', 'ativo': False},
    '33333333333': {'nome': 'Almeida', 'senha': '123456', 'telefone': '83982828282', 'tipo': 'paciente', 'observacoes': '', 'alergias': ''},
}
consultorios = [{'id': 1, 'nome': 'Sala 1', 'dentistas': ['22222222222', '44444444444']}]
consultas = []

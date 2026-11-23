# clinDONTO — Clínica odontológica

Projeto de Algoritmos conforme `instrucoes.pdf`: aplicação Python com menus
numéricos no terminal, funções, listas e dicionários em memória. Usa o pacote
externo **tabulate** para apresentar tabelas.

## Executar

Requer Python 3.10 ou superior, pip e suporte a ambientes virtuais.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install tabulate==0.9.0
python main.py
```

Neste ambiente, a dependência está instalada em `.venv`; execute:

```bash
.venv/bin/python main.py
```

## Contas de demonstração

| Perfil | CPF | Senha |
| --- | --- | --- |
| Administrador | 11111111111 | 123456 |
| Paciente | 33333333333 | 123456 |

Os CPFs são fictícios. A validação exige 11 números, sem verificar os dígitos
verificadores. Um CPF novo no módulo paciente oferece autocadastro com nome,
senha e telefone. CPF e senha são obrigatórios para entrar em contas existentes.

## Funcionalidades

- Paciente: corpo clínico ativo, agendamento, consultas futuras próprias,
  cancelamento próprio, atualização de dados e histórico pessoal.
- Secretaria: cadastrar, listar, buscar, atualizar e remover dentistas e pacientes;
  registrar observações e alergias; cadastrar salas e vincular/desvincular dentistas;
  consultar agenda geral, filtrar por dentista/data e cancelar consultas futuras.
- Extra administrativo: resumo com pacientes, dentistas ativos, salas e consultas futuras.

Cada consulta dura **60 minutos**. Datas usam `DD/MM/AAAA HH:MM` e o horário local
do computador. Sobreposições são bloqueadas para o dentista, o paciente e a sala,
mesmo quando o início das consultas difere. Horários consecutivos são permitidos.
Somente dentistas ativos vinculados à sala podem receber agendamentos.
Cancelamentos liberam o horário e ficam no histórico. Consultas passadas não
podem ser canceladas. Cadastros com consultas futuras não podem ser removidos;
dentistas nessa situação também não podem ser inativados ou desvinculados da
sala com consultas futuras.

Os dados são reiniciados a cada execução, conforme o armazenamento em memória
pedido no PDF. Senhas em texto simples e contas fictícias destinam-se à atividade
acadêmica. Não há persistência nem integração com serviços externos.

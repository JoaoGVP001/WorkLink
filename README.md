# Worklink

O Worklink é um trabalho da disciplina Programação Orientada a Objetos I, no IFC Campus Concórdia. A ideia é criar um sistema simples para divulgar vagas de emprego e permitir que candidatos se inscrevam.

## Como funciona

- **Candidato:** monta seu perfil profissional, procura vagas e acompanha suas candidaturas.
- **Recrutador:** publica vagas da empresa e avalia as candidaturas recebidas.
- **Administrador:** cadastra empresas e contas de recrutadores e administra os vínculos entre eles.

Cada candidatura tem uma situação, como enviada, em análise, aprovada, rejeitada ou cancelada. O sistema também verifica regras como o prazo da vaga e a inscrição duplicada do mesmo candidato.

## O que estamos aprendendo

O projeto usa classes e objetos para representar as partes do sistema. A classe `User` é abstrata e serve de base para os tipos de usuário. Cada tipo tem permissões próprias. Também usamos propriedades para controlar o acesso aos dados e relações entre candidatos, perfis, empresas, vagas e candidaturas.

## Versão atual

O sistema está sendo feito em Python. A demonstração do backend continua disponível pelo console, e a janela inicial da interface Tkinter é aberta por `app.py`. Os dados ficam guardados apenas enquanto o programa está aberto.

## Abrir a janela do sistema

Com o Python instalado, abra um terminal nesta pasta e execute:

```bash
python3 app.py
```

A janela começa com um administrador de demonstração. A opção de selecionar usuário serve para trocar o perfil usado na demonstração; não é um sistema de login. Os dados continuam apenas na memória enquanto o programa está aberto.

**Grupo:** João Guilherme, Arthur, Rafael e Lucas.

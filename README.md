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

O sistema está sendo feito em Python. Nesta etapa, a demonstração é pelo console e os dados ficam guardados apenas enquanto o programa está aberto. A interface gráfica com Tkinter está prevista para a próxima parte do trabalho.

**Grupo:** João Guilherme, Arthur, Rafael e Lucas.

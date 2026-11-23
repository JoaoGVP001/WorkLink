# WorkLink

O WorkLink é um projeto da disciplina de Programação Orientada a Objetos I do IFC Campus Concórdia. O sistema permite divulgar vagas de emprego e estágio, receber inscrições e acompanhar o resultado das candidaturas.

## Como executar

Com Python 3 e Tkinter disponíveis, abra um terminal na pasta do projeto e rode `python3 app.py`.

A tela inicial exibe duas vagas de exemplo com inscrições até **31/01/2027**. A escolha de contas serve para demonstrar os perfis. Os dados ficam em memória durante a execução.

## O que cada perfil pode fazer

- **Candidato** — consulta vagas, edita o perfil profissional, envia candidaturas e acompanha ou cancela inscrições pendentes.
- **Recrutador** — cadastra, edita e encerra vagas da própria empresa, exclui vagas sem inscrições e avalia candidaturas.
- **Administrador** — cadastra empresas e contas, vincula recrutadores a empresas e gerencia a situação das contas.

## Demonstração rápida

1. Selecione uma vaga e clique em **Quero me candidatar**. Cadastre um candidato e confirme a inscrição.
2. Abra a **Área da empresa**, escolha **João Teste** e avalie a inscrição na aba **Candidaturas**.
3. Volte à **Área do candidato** e confira a nova situação em **Minhas Candidaturas**.

## Organização do código

- `app.py` abre a interface. A pasta `ui` reúne as telas do Tkinter.
- `models.py` e `services.py` concentram as classes e as regras, como o prazo da vaga e o bloqueio de inscrições duplicadas. A classe abstrata `User` define o método de permissões que cada perfil implementa.
- `main.py` mantém a demonstração da Parte 2 pelo console. Para rodar, use `python3 main.py`.

**Grupo:** João Guilherme, Arthur, Rafael e Lucas.

from flask import request, flash, redirect, url_for
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session, Time


def select_todos():
    # 1 - Montar o select
    # join(Tabela que eu quero juntar, condição = chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2 - Executar o select
    # usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    print(jogadores)

    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

print(select_quantidade_total())

def novo_jogador():
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa", "").strip()
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id", "").strip()

        # 2 - Verificar se foi digitado
        if not nome:
            flash('Preencha o nome', 'error')
            return redirect(url_for(novo_jogador))
        if not numero_camisa:
            flash('Preencha o número da camisa', 'error')
            return redirect(url_for(novo_jogador))
        if not posicao:
            flash('Preencha a posição', 'error')
            return redirect(url_for(novo_jogador))
        if not time_id:
            flash('Preencha o time', 'error')
            return redirect(url_for(novo_jogador))

        # 3 - Salvar no banco
        try:
            jogador_novo = Jogador(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=int(time_id))
            db_session.add(jogador_novo)
            db_session.commit()
            flash("Jogador cadastrado com sucesso", 'success')
        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", 'error')
            print(f"Erro: {e}")
        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", 'error')
            print(f"Erro: {e}")
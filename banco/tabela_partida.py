from flask import request, flash, redirect, url_for
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Partida, Time


def select_novo(times_sql=None):
    # 2 - Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    partidas_sql = select(Partida)
    # 2 - Executar o select
    partidas = db_session.execute(partidas_sql).scalars().all()
    print(partidas)

def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # 2 - Verificar se foi digitado
        if not time_casa_id:
            flash('Preencha o timeda casa', 'error')
            return redirect(url_for(nova_partida))
        if not time_visitante_id:
            flash('Preencha o time visitante', 'error')
            return redirect(url_for(nova_partida))
        if not gols_casa:
            flash('Preencha o total de gols do time da casa', 'error')
            return redirect(url_for(nova_partida))
        if not gols_visitante:
            flash('Preencha o total de gols do time visitante', 'error')
            return redirect(url_for(nova_partida))
        if not data_partida:
            flash('Preencha a data da partida', 'error')
            return redirect(url_for(nova_partida))

        # 3 - Verificar se os times são iguais
        if time_casa_id and time_visitante_id:
            flash('Selecione times diferentes', 'error')
            return redirect(url_for(nova_partida))

        # 4 - Salvar no banco
        try:
            partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id,gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
            db_session.add(partida_nova)
            db_session.commit()
            flash("Partida criada com sucesso", 'success')

        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", 'error')
            print(f"Erro: {e}")
        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", 'error')
            print(f"Erro: {e}")
            # Buscar todos os times do banco
            # 1 - Montar o select
    times_sql = select(Time)

from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_partida, tabela_jogador
from database import Jogador,Time,db_session,Partida

app = Flask(__name__)
app.secret_key = "vtzika"


@app.route("/")
def dashboard():
    # Buscar todos os times do banco
    # 1 - Montar o select
    times_sql = select(Time)

    # 2 - Executar o select
    times = tabela_time.select_quantidade_total()
    jogadores_sql = select(Jogador)

    # 2 - Executar o select
    jogadores = tabela_jogador.select_quantidade_total()
    select(Partida)

    # 2 - Executar o select
    partidas = tabela_partida.select_quantidade_total()
    print(partidas)

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores_sql = select(Jogador)
    # 2 - Executar o select
    jogadores = [db_session.execute(jogadores_sql).scalars().all()]
    return render_template("jogadores.html", jogadores=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
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
            return redirect(url_for('novo_jogador'))
        if not numero_camisa:
            flash('Preencha o número da camisa', 'error')
            return redirect(url_for('novo_jogador'))
        if not posicao:
            flash('Preencha a posição', 'error')
            return redirect(url_for('novo_jogador'))
        if not time_id:
            flash('Preencha o time', 'error')
            return redirect(url_for('novo_jogador'))

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

    # Buscar todos os times do banco

    # 1 - Montar o select
    jogadores_sql = select(Jogador)

    # 2 - Executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    print(jogadores)
    times_sql = select(Time)


    # 2 - Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)

    return render_template("jogadores.html", times=times)


@app.route("/times")
def listar_times():
    # Buscar todos os times do banco
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        # 2 - Verificar se foi digitado
        if not nome:
            flash('Preencha o nome', 'error')
            return redirect(url_for(novo_time))
        if not turma:
            flash('Preencha a turma', 'error')
            return redirect(url_for(novo_time))
        if not responsavel:
            flash('Preencha o responsável', 'error')
            return redirect(url_for(novo_time))

        # 3 - Salvar no banco
        tabela_time.salvar(nome, turma, responsavel)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    partidas_sql = select(Partida)

    # 2 - Executar o select
    partidas = db_session.execute(partidas_sql).scalars().all()
    print(partidas)

    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # 2 - Verificar se foi digitado
        if not time_casa_id:
            flash('Preencha o time da casa', 'error')
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
            return redirect(url_for("nova_partida"))

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

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
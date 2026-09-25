import flask
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=0,
        total_partidas=0,
        proximas_partidas=0,
        times_ranking=0,
    )


@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        numero_camisa = request.form.get("numero_camisa") or None

        if not nome:
            flash("Preencha o nome"), "error"
            return render_template("jogadores.html")

        if not posicao:
            flash("Preencha a posição"), "error"
            return render_template("jogadores.html")

        if not time_id:
            flash("Preencha o time"), "error"
            return render_template("jogadores.html")

        if not numero_camisa:
            flash("Preencha o numero_camisa"), "error"
            return render_template("jogadores.html")

        try:
            novo_jogador = Jogadores(nome=nome, posicao=posicao, time_id=time_id, numero_camisa=numero_camisa)
            db_session.add(novo_jogador)
            db_session.commit()
            flash("Jogador adicionado com sucesso", "success")

        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

    return render_template("jogadores.html", jogadores=[], times=[])


@app.route("/times")
def listar_times():

    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel") or None
        turma = request.form.get("turma") or None

        if not nome:
            flash("Preencha o nome"), "error"
            return render_template("times.html")

        if not turma:
            flash("Preencha a turma"), "error"
            return render_template("times.html")

        if not responsavel:
            flash("Preencha o responsável"), "error"
            return render_template("times.html")

        try:
            novo_time = Time(nome=nome, responsavel=responsavel, turma=turma)
            db_session.add(novo_time)
            db_session.commit()
            flash("Time criado com sucesso", "success")

        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("placar_casa") or 0
        gols_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        if not time_casa_id:
            flash("Preencha o time da casa"), "error"
            return render_template("partidas.html")

        if not time_visitante_id:
            flash("Preencha o time visitante"), "error"
            return render_template("partidas.html")

        if not gols_casa:
            flash("Preencha os gols da casa"), "error"
            return render_template("partidas.html")

        if not gols_visitante:
            flash("Preencha os gols do visitante"), "error"
            return render_template("partidas.html")

        if not data_partida:
            flash("Preencha o data da partida"), "error"
            return render_template("partidas.html")

        try:
            nova_partida = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa,
                                   gols_visitante=gols_visitante, data_partida=data_partida)
            db_session.add(nova_partida)
            db_session.commit()
            flash("Informações adicionadas com sucesso", "success")

        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

    return render_template("partidas.html", partidas=[], times=[])


if __name__ == "__main__":
    app.run(debug=True)

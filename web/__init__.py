from flask import Flask, render_template
import os
from dotenv import load_dotenv

from database.database import SessionLocal, Registro, agora, formatar_dt, formatar_duracao, formatar_segundos
load_dotenv()

PORT = os.getenv("PORT")
app = Flask(__name__)
app.config['TEMPLATES_FOLDER'] = os.path.join(os.path.dirname(__file__), 'templates')
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/')
def dashboard():
    session = SessionLocal()
    try:
        registros_db = session.query(Registro).order_by(Registro.id.desc()).all()
        usuarios_resumo = {}
        
        for r in registros_db:
            uid = r.user_id
            
            if uid not in usuarios_resumo:
                usuarios_resumo[uid] = {
                    'nome': r.usuario,
                    'apelido': r.nome or r.usuario,
                    'total_segundos': 0,
                    'registros': [],
                    'em_andamento': False
                }
            
            data_ent, hora_ent = formatar_dt(r.entrada)
            
            if r.saida:
                duracao = r.saida - r.entrada
                usuarios_resumo[uid]['total_segundos'] += int(duracao.total_seconds())
                hora_sai = formatar_dt(r.saida)[1]
                total_str = formatar_duracao(duracao)
            else:
                hora_sai = "aberto"
                total_str = "Em andamento"
                usuarios_resumo[uid]['em_andamento'] = True
                
            usuarios_resumo[uid]['registros'].append({
                'id': r.id, 'data': data_ent, 'entrada': hora_ent,
                'saida': hora_sai, 'total': total_str, 'observacao': r.observacao or ""
            })
            
        for uid, dados in usuarios_resumo.items():
            dados['total_formatado'] = formatar_segundos(dados['total_segundos'])
            
        return render_template('index.html', usuarios=usuarios_resumo)
    finally:
        session.close()

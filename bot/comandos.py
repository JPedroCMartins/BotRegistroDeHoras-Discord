import discord
from discord import app_commands
from discord.ext import commands
from database.database import SessionLocal, Registro, agora, formatar_dt, formatar_duracao, formatar_segundos
class Comandos():
    def __init__(self, tree):
        self.tree = tree

        @tree.command(name="entrada", description="Registra seu horário de entrada")
        @app_commands.describe(nome="Obrigatório apenas na PRIMEIRA vez", observacao="Observação opcional")
        async def entrada(interaction: discord.Interaction, nome: str = None, observacao: str = ""):
            user_id = str(interaction.user.id)
            session = SessionLocal()
            
            try:
                # Lógica de memória do nome
                registro_anterior = session.query(Registro).filter_by(user_id=user_id).first()
                
                if registro_anterior and registro_anterior.nome:
                    nome_final = registro_anterior.nome
                    tentou_mudar = (nome is not None and nome.lower() != nome_final.lower())
                else:
                    if not nome:
                        await interaction.response.send_message(
                            "❌ Como é sua **primeira vez**, você precisa informar um `nome`!\n"
                            "Exemplo: `/entrada nome: João Carlos`", ephemeral=True
                        )
                        return
                        
                    nome_em_uso = session.query(Registro).filter(Registro.nome.ilike(nome), Registro.user_id != user_id).first()
                    if nome_em_uso:
                        await interaction.response.send_message(f"❌ O nome **{nome}** já está registrado por outra pessoa.", ephemeral=True)
                        return
                        
                    nome_final = nome
                    tentou_mudar = False

                # Verifica jornada aberta
                registro_aberto = session.query(Registro).filter_by(user_id=user_id, saida=None).first()
                if registro_aberto:
                    await interaction.response.send_message("Você já tem uma entrada aberta. Use /saida primeiro.", ephemeral=True)
                    return
                
                # Salva no banco
                dt_entrada = agora()
                novo_registro = Registro(
                    user_id=user_id, usuario=str(interaction.user.name), nome=nome_final,
                    entrada=dt_entrada, observacao=observacao
                )
                session.add(novo_registro)
                session.commit()
                
                # Feedback
                data_str, hora_str = formatar_dt(dt_entrada)
                embed = discord.Embed(title="Entrada Registrada", color=discord.Color.green())
                embed.add_field(name="Usuário", value=interaction.user.name, inline=True)
                embed.add_field(name="Nome", value=nome_final, inline=True)
                embed.add_field(name="Data", value=data_str, inline=True)
                embed.add_field(name="Hora", value=hora_str, inline=True)
                if observacao: embed.add_field(name="Observação", value=observacao, inline=False)
                    
                aviso = f"\n*⚠️ Nota: Seu nome definitivo é **{nome_final}**.*" if tentou_mudar else ""
                await interaction.response.send_message(content=aviso, embed=embed)
            finally:
                session.close()

        @tree.command(name="saida", description="Registra seu horário de saída")
        async def saida(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            session = SessionLocal()
            
            try:
                registro = session.query(Registro).filter_by(user_id=user_id, saida=None).first()
                if not registro:
                    await interaction.response.send_message("Nenhuma entrada aberta. Use /entrada primeiro.", ephemeral=True)
                    return
                
                dt_saida = agora()
                registro.saida = dt_saida
                session.commit()
                
                tempo_total = formatar_duracao(dt_saida - registro.entrada)
                embed = discord.Embed(title="Saída Registrada", color=discord.Color.red())
                nome_exibicao = registro.nome if registro.nome else interaction.user.name
                embed.add_field(name="Usuário", value=nome_exibicao, inline=True)
                embed.add_field(name="Total trabalhado", value=tempo_total, inline=True)
                await interaction.response.send_message(embed=embed)
            finally:
                session.close()

        @tree.command(name="status", description="Verifica se você tem entrada ativa")
        async def status(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            session = SessionLocal()
            try:
                registro = session.query(Registro).filter_by(user_id=user_id, saida=None).first()
                if registro:
                    duracao = agora() - registro.entrada
                    embed = discord.Embed(title="Você está em jornada", color=discord.Color.green())
                    embed.add_field(name="Entrada em", value=formatar_dt(registro.entrada)[1], inline=True)
                    embed.add_field(name="Tempo acumulado", value=formatar_duracao(duracao), inline=True)
                else:
                    embed = discord.Embed(title="Sem jornada ativa", description="Use /entrada para iniciar.", color=discord.Color.greyple())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            finally:
                session.close()

        @tree.command(name="historico", description="Exibe seus últimos registros")
        @app_commands.describe(quantidade="Quantos registros exibir (padrão 5)")
        async def historico(interaction: discord.Interaction, quantidade: int = 5):
            user_id = str(interaction.user.id)
            session = SessionLocal()
            try:
                registros = session.query(Registro).filter_by(user_id=user_id).order_by(Registro.id.desc()).limit(min(quantidade, 15)).all()
                if not registros:
                    await interaction.response.send_message("Nenhum registro encontrado.", ephemeral=True)
                    return
                
                embed = discord.Embed(title=f"Histórico de {interaction.user.name}", color=discord.Color.blue())
                for r in registros:
                    data_ent, hora_ent = formatar_dt(r.entrada)
                    _, hora_sai = formatar_dt(r.saida) if r.saida else ("-", "aberto")
                    total = formatar_duracao(r.saida - r.entrada) if r.saida else "-"
                    info_nome = f" ({r.nome})" if r.nome else ""
                    embed.add_field(name=f"{data_ent}{info_nome}", value=f"Entrada: `{hora_ent}` | Saída: `{hora_sai}` | Total: `{total}`", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            finally:
                session.close()
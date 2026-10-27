import os
import re
import time
import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# ==========================================
# CREDENCIAIS E CONFIGURAÇÕES
# ==========================================
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"
NOME_USUARIO = "Aluno TI"
NOME_BOT = "TechBot IA"


# ==========================================
# BASE DE CONHECIMENTO MULTI-TEMAS (LOCAL)
# ==========================================
BASE_CONHECIMENTO = {
    "historia": [
        (r'descobridor do brasil|quem descobriu o brasil|pedro alvares cabral', 
         "O Brasil foi achado em 1500 pela expedição portuguesa comandada por Pedro Álvares Cabral."),
        (r'primeiro presidente do brasil|deodoro da fonseca', 
         "O primeiro presidente do Brasil foi o Marechal Deodoro da Fonseca (1889-1891)."),
        (r'segunda guerra mundial|2 guerra', 
         "A Segunda Guerra Mundial ocorreu entre 1939 e 1945, terminando com a vitória dos Aliados."),
        (r'homem mais importante|pessoa mais influente', 
         "Historiadores destacam figuras como Jesus de Nazaré, Isaac Newton, Albert Einstein e Maomé como algumas das mais influentes da história humanidade.")
    ],
    "geografia": [
        (r'presidente dos estados unidos|presidente do eua|presidente eua', 
         "O presidente dos Estados Unidos é Joe Biden (com Donald Trump eleito para o próximo mandato nas eleições de 2024)."),
        (r'presidente do brasil', 
         "O atual presidente do Brasil é Luiz Inácio Lula da Silva."),
        (r'capital do brasil', 
         "A capital do Brasil é Brasília, localizada no Distrito Federal."),
        (r'maior pais do mundo', 
         "O maior país do mundo em área territorial é a Rússia."),
        (r'qual e o maior oceano', 
         "O maior oceano do planeta é o Oceano Pacífico.")
    ],
    "entretenimento": [
        (r'rei dos animais|rei do animais|filme dele', 
         "O animal considerado o 'Rei dos Animais' é o Leão, que protagoniza o clássico filme 'O Rei Leão' da Disney."),
        (r'filme mais assistido|maior bilheteria', 
         "O filme de maior bilheteria e mais visto nos cinemas mundialmente é Avatar (2009), seguido por Vingadores: Ultimato e Titanic."),
        (r'jogo mais jogado|game mais popular', 
         "Atualmente, jogos como Roblox, Minecraft e Fortnite lideram em número de jogadores ativos no mundo.")
    ],
    "ciencia_tecnologia": [
        (r'o que e python|linguagem python', 
         "Python é uma linguagem de programação de alto nível, interpretada, de sintaxe simples e amplamente usada em Inteligência Artificial e desenvolvimento web."),
        (r'o que e inteligencia artificial|o que e ia', 
         "Inteligência Artificial (IA) é o campo da ciência da computação focado em criar sistemas capazes de realizar tarefas que normalmente exigem inteligência humana."),
        (r'velocidade da luz', 
         "A velocidade da luz no vácuo é de aproximadamente 300.000 km por segundo (299.792.458 m/s).")
    ],
    "idiomas": [
        (r'viver em ingles|como e viver em ingles', 
         "Em inglês, o verbo viver/morar é 'to live'. Exemplo: 'I live in Brazil' (Eu vivo no Brasil)."),
        (r'obrigado em ingles', 
         "Obrigado em inglês é 'Thank you' ou 'Thanks'."),
        (r'bom dia em ingles', 
         "Bom dia em inglês é 'Good morning'.")
    ]
}


# ==========================================
# TELA DE LOGIN
# ==========================================
class TelaLogin:
    def __init__(self, root, callback_sucesso):
        self.root = root
        self.callback_sucesso = callback_sucesso
        self.root.title("Login - Sistema de Chatbot IA")
        self.root.geometry("380x450")
        self.root.resizable(False, False)

        self.frame = ttk.Frame(self.root, padding=30)
        self.frame.pack(expand=True, fill=BOTH)

        lbl_titulo = ttk.Label(self.frame, text="Portal de Acesso", font=("Helvetica", 18, "bold"))
        lbl_titulo.pack(pady=(0, 20))

        ttk.Label(self.frame, text="Usuário:", font=("Helvetica", 10)).pack(anchor=W, pady=(5, 2))
        self.ent_usuario = ttk.Entry(self.frame, font=("Helvetica", 11))
        self.ent_usuario.pack(fill=X, pady=(0, 15))
        self.ent_usuario.insert(0, "admin")

        ttk.Label(self.frame, text="Senha:", font=("Helvetica", 10)).pack(anchor=W, pady=(5, 2))
        self.ent_senha = ttk.Entry(self.frame, show="•", font=("Helvetica", 11))
        self.ent_senha.pack(fill=X, pady=(0, 20))
        self.ent_senha.insert(0, "1234")

        btn_login = ttk.Button(self.frame, text="Entrar no Chat", bootstyle=PRIMARY, command=self.validar_login)
        btn_login.pack(fill=X, pady=10)
        
        self.root.bind("<Return>", lambda e: self.validar_login())

    def validar_login(self):
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()

        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            self.frame.destroy()
            self.root.unbind("<Return>")
            self.callback_sucesso()
        else:
            messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos!\nCredenciais padrão: admin / 1234")


# ==========================================
# TELA PRINCIPAL DO CHAT
# ==========================================
class TelaChat:
    def __init__(self, root):
        self.root = root
        self.root.title("Curso Técnico DS - IA Própria (TechBot)")
        self.root.geometry("700x750")
        self.root.minsize(500, 500)

        self.modo_escuro = True

        self.main_container = ttk.Frame(self.root, padding=15)
        self.main_container.pack(fill=BOTH, expand=True)

        self.criar_cabecalho()
        self.criar_area_chat()
        self.criar_controles_entrada()

        self.adicionar_mensagem(NOME_BOT, "🤖", 
            "Olá! Sou o TechBot IA. Posso te ajudar com vários temas:\n"
            "• História & Geografia\n"
            "• Entretenimento & Filmes\n"
            "• Tecnologia & Programação\n"
            "• Cálculos & Idiomas\n\n"
            "Faça sua pergunta!", "bot")

    def criar_cabecalho(self):
        header = ttk.Frame(self.main_container)
        header.pack(fill=X, pady=(0, 10))

        lbl_titulo = ttk.Label(header, text="💬 TechBot IA - Assistente Inteligente", font=("Helvetica", 14, "bold"))
        lbl_titulo.pack(side=LEFT)

        self.btn_tema = ttk.Button(header, text="☀️ Alternar Tema", bootstyle=OUTLINE, command=self.alternar_tema)
        self.btn_tema.pack(side=RIGHT)

    def criar_area_chat(self):
        chat_frame = ttk.Frame(self.main_container)
        chat_frame.pack(fill=BOTH, expand=True, pady=(0, 10))

        self.canvas = tk.Canvas(chat_frame, highlightthickness=0, bg="#1e1e1e")
        self.scrollbar = ttk.Scrollbar(chat_frame, orient=VERTICAL, command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=e.width))

    def criar_controles_entrada(self):
        input_frame = ttk.Frame(self.main_container)
        input_frame.pack(fill=X)

        self.ent_mensagem = ttk.Entry(input_frame, font=("Helvetica", 11))
        self.ent_mensagem.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.ent_mensagem.bind("<Return>", lambda e: self.enviar_mensagem())

        btn_enviar = ttk.Button(input_frame, text="Enviar", bootstyle=SUCCESS, command=self.enviar_mensagem)
        btn_enviar.pack(side=LEFT, padx=(0, 5))

        btn_limpar = ttk.Button(input_frame, text="Limpar", bootstyle=DANGER, command=self.limpar_chat)
        btn_limpar.pack(side=LEFT)

    def adicionar_mensagem(self, nome, icone, texto, tipo="user"):
        msg_frame = ttk.Frame(self.scrollable_frame, padding=5)
        msg_frame.pack(fill=X, expand=True, pady=5, padx=10)

        user_bg = "#0d6efd"
        bot_bg = "#343a40" if self.modo_escuro else "#f8f9fa"
        text_color = "#ffffff" if (tipo == "user" or self.modo_escuro) else "#212529"

        if tipo == "user":
            header_text = f"{nome} {icone}"
            bubble = tk.Label(
                msg_frame, text=f"{header_text}\n{texto}",
                bg=user_bg, fg="#ffffff", font=("Helvetica", 10),
                justify=RIGHT, wraplength=450, padx=12, pady=8, anchor="e"
            )
            bubble.pack(side=RIGHT, anchor="e")
        else:
            header_text = f"{icone} {nome}"
            bubble = tk.Label(
                msg_frame, text=f"{header_text}\n{texto}",
                bg=bot_bg, fg=text_color, font=("Helvetica", 10),
                justify=LEFT, wraplength=450, padx=12, pady=8, anchor="w",
                relief="solid", bd=1
            )
            bubble.pack(side=LEFT, anchor="w")

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def enviar_mensagem(self):
        texto = self.ent_mensagem.get().strip()
        if not texto:
            return

        self.ent_mensagem.delete(0, END)
        self.adicionar_mensagem(NOME_USUARIO, "👤", texto, "user")

        threading.Thread(target=self.gerar_resposta_ia, args=(texto,), daemon=True).start()

    def gerar_resposta_ia(self, pergunta):
        pergunta_clean = pergunta.lower().strip()
        # Remove acentos básicos e pontuações para facilitar a busca
        pergunta_norm = re.sub(r'[áàãâ]', 'a', pergunta_clean)
        pergunta_norm = re.sub(r'[éê]', 'e', pergunta_norm)
        pergunta_norm = re.sub(r'[í]', 'i', pergunta_norm)
        pergunta_norm = re.sub(r'[óõô]', 'o', pergunta_norm)
        pergunta_norm = re.sub(r'[ú]', 'u', pergunta_norm)
        pergunta_norm = re.sub(r'[ç]', 'c', pergunta_norm)
        
        resposta = None

        # 1. CÁLCULO LOCAL DE DATAS E IDADES
        ano_atual = datetime.datetime.now().year
        match_ano = re.search(r'(?:nasc\w+|ano)\s+(?:em|de|no\s+ano)?\s*(\d{3,4})', pergunta_norm) or re.search(r'em\s+(\d{3,4})', pergunta_norm)
        if match_ano and any(w in pergunta_norm for w in ["ano", "idade", "nasc", "teria", "ter"]):
            ano_nasc = int(match_ano.group(1))
            resposta = f"Se você nascesse em {ano_nasc}, teria {ano_atual - ano_nasc} anos no ano atual ({ano_atual})."

        # 2. OPERAÇÕES MATEMÁTICAS DIRETAS
        elif any(op in pergunta_norm for op in ['+', '-', '*', '/']) and re.search(r'\d+', pergunta_norm):
            try:
                expressao = re.sub(r'[^0-9\+\-\*\/\.]', '', pergunta_norm)
                if expressao:
                    resultado = eval(expressao)
                    resposta = f"O resultado da operação matemática é: {resultado}"
            except Exception:
                pass

        # 3. BUSCA INTELIGENTE NA BASE MULTI-TEMAS
        if not resposta:
            for categoria, padroes in BASE_CONHECIMENTO.items():
                for padrao, resp in padroes:
                    if re.search(padrao, pergunta_norm):
                        resposta = resp
                        break
                if resposta:
                    break

        # 4. RESPOSTA AMIGÁVEL DE AJUDA COM SUGESTÕES DE TEMAS
        if not resposta:
            resposta = (
                f"Ainda não tenho a resposta exata para '{pergunta}', mas posso te ajudar com:\n\n"
                "• 'Quem é o presidente dos Estados Unidos?'\n"
                "• 'Qual é o rei dos animais?'\n"
                "• 'Quem foi Pedro Álvares Cabral?'\n"
                "• 'Qual é o filme mais assistido?'\n"
                "• 'Se eu nascesse em 2000, quantos anos teria?'\n"
                "• Cálculos matemáticos (Ex: 15 + 35 * 2)"
            )

        # Pequeno delay simulando processamento humano/IA
        time.sleep(0.3)
        self.root.after(0, lambda: self.adicionar_mensagem(NOME_BOT, "🤖", resposta, "bot"))

    def limpar_chat(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.adicionar_mensagem(NOME_BOT, "🤖", "Conversa limpa! Como posso ajudar agora?", "bot")

    def alternar_tema(self):
        if self.modo_escuro:
            ttk.Style().theme_use("flatly")
            self.canvas.configure(bg="#ffffff")
            self.modo_escuro = False
        else:
            ttk.Style().theme_use("darkly")
            self.canvas.configure(bg="#1e1e1e")
            self.modo_escuro = True


# ==========================================
# EXECUÇÃO DA APLICAÇÃO
# ==========================================
def main():
    app = ttk.Window(themename="darkly")
    
    def iniciar_chat():
        TelaChat(app)

    TelaLogin(app, callback_sucesso=iniciar_chat)
    app.mainloop()

if __name__ == "__main__":
    main()
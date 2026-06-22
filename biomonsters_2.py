import tkinter as tk
from tkinter import messagebox
import random

# ==============================================================
#  LÓGICA DO JOGO  —  POO com Herança e Polimorfismo
# ==============================================================

class Ataque:
    """Representa um ataque que um Monstrinho pode usar."""
    def __init__(self, nome: str, dano_base: int, custo_pe: int):
        self.nome = nome
        self.dano_base = dano_base
        self.custo_pe = custo_pe

    def __str__(self):
        return f"{self.nome} (Dano: {self.dano_base} | PE: {self.custo_pe})"


# ──────────────────────────────────────────────────────────────
#  CLASSE BASE
# ──────────────────────────────────────────────────────────────

class Monstrinho:
    """
    Classe base para todos os Bio-Monsters.
    Define a interface comum; subclasses sobrescrevem os métodos
    marcados com #[POLIMORFISMO].
    """

    def __init__(self, nome: str, tipo: str, hp_max: int,
                 defesa: int, velocidade: int, ataques: list):
        self.nome = nome
        self.tipo = tipo
        self.hp_max = hp_max
        self.hp_atual = hp_max
        self.defesa = defesa
        self.velocidade = velocidade
        self.pe_max = 50
        self.pe_atual = 50
        self.ataques = ataques

    # ── Métodos comuns ──────────────────────────────────────

    def clonar(self):
        """Cria uma cópia fresca do monstrinho para cada batalha."""
        novo = self.__class__(
            self.nome, self.hp_max,
            self.defesa, self.velocidade, self.ataques
        )
        return novo

    def esta_vivo(self) -> bool:
        return self.hp_atual > 0

    def receber_dano(self, dano_bruto: int) -> int:
        """Aplica a redução de defesa e desconta o HP."""
        dano_real = max(1, dano_bruto - self.reducao_defesa())   # [POLIMORFISMO]
        self.hp_atual = max(0, self.hp_atual - dano_real)
        return dano_real

    def usar_ataque(self, ataque: Ataque, alvo: "Monstrinho") -> str:
        """Executa um ataque contra o alvo e retorna o log da ação."""
        if self.pe_atual >= ataque.custo_pe:
            self.pe_atual -= ataque.custo_pe
            multiplicador, msg_vantagem = self.calcular_vantagem(alvo.tipo)  # [POLIMORFISMO]
            dano_final = int(ataque.dano_base * multiplicador * self.bonus_ataque())  # [POLIMORFISMO]
            dano_causado = alvo.receber_dano(dano_final)
            return (f"{self.nome} usou {ataque.nome}!\n"
                    f"{msg_vantagem}Causou {dano_causado} de dano em {alvo.nome}.")
        else:
            # Sem PE → Investida Cega com recuo
            recuo = self.dano_recuo()                                         # [POLIMORFISMO]
            self.hp_atual = max(0, self.hp_atual - recuo)
            dano_causado = alvo.receber_dano(10)
            return (f"⚠️ {self.nome} tentou usar {ataque.nome}, mas está sem PE!\n"
                    f"Em desespero, usou Investida Cega!\n"
                    f"Causou {dano_causado} de dano em {alvo.nome} e sofreu {recuo} de recuo!")

    # ── Métodos polimórficos (sobrescritos pelas subclasses) ─

    def calcular_vantagem(self, tipo_defensor: str) -> tuple:
        """[POLIMORFISMO] Retorna (multiplicador, mensagem) com base na tipagem."""
        tabela = {
            ("Vírus",   "Bactéria"): (1.5, "✨ Super efetivo! "),
            ("Bactéria","Fungo"):    (1.5, "✨ Super efetivo! "),
            ("Fungo",   "Vírus"):   (1.5, "✨ Super efetivo! "),
            ("Vírus",   "Fungo"):   (0.5, "🍃 Pouco efetivo... "),
            ("Bactéria","Vírus"):   (0.5, "🍃 Pouco efetivo... "),
            ("Fungo",   "Bactéria"):(0.5, "🍃 Pouco efetivo... "),
        }
        if self.tipo == tipo_defensor:
            return (0.8, "🔵 Pouco efetivo (mesmo tipo)... ")
        return tabela.get((self.tipo, tipo_defensor), (1.0, ""))

    def reducao_defesa(self) -> int:
        """[POLIMORFISMO] Quanto da defesa é subtraído do dano recebido."""
        return self.defesa // 2

    def bonus_ataque(self) -> float:
        """[POLIMORFISMO] Multiplicador extra de ataque (padrão: sem bônus)."""
        return 1.0

    def dano_recuo(self) -> int:
        """[POLIMORFISMO] Dano que o próprio monstrinho sofre ao usar Investida Cega."""
        return 5

    def habilidade_passiva_descricao(self) -> str:
        """[POLIMORFISMO] Texto descritivo da habilidade passiva para a UI."""
        return "Sem habilidade passiva."

    def __str__(self):
        return (f"{self.nome} [{self.tipo}] "
                f"HP:{self.hp_atual}/{self.hp_max} PE:{self.pe_atual}/{self.pe_max}")


# ──────────────────────────────────────────────────────────────
#  SUBCLASSES  —  Herança + Polimorfismo
# ──────────────────────────────────────────────────────────────

class Virus(Monstrinho):
    """
    [HERANÇA] Vírus são rápidos e causam dano extra, mas têm menos HP.
    Habilidade passiva: Mutação — cada ataque tem 20% de chance de
    ignorar completamente a defesa do alvo.
    """

    def __init__(self, nome, hp_max, defesa, velocidade, ataques):
        super().__init__(nome, "Vírus", hp_max, defesa, velocidade, ataques)

    def bonus_ataque(self) -> float:
        """[POLIMORFISMO] 20% de chance de ataque crítico (ignora defesa via bonus)."""
        if random.random() < 0.20:
            return 1.35   # acerto crítico
        return 1.0

    def dano_recuo(self) -> int:
        """[POLIMORFISMO] Vírus sofrem mais recuo por serem frágeis."""
        return 8

    def habilidade_passiva_descricao(self) -> str:
        return "🧬 Mutação: 20% de chance de acerto crítico (+35% dano)."


class Bacteria(Monstrinho):
    """
    [HERANÇA] Bactérias são equilibradas com capacidade de regenerar PE.
    Habilidade passiva: Fissão — recupera 5 PE ao final de cada turno
    em que causou dano.
    """

    def __init__(self, nome, hp_max, defesa, velocidade, ataques):
        super().__init__(nome, "Bactéria", hp_max, defesa, velocidade, ataques)
        self._causou_dano_no_turno = False

    def usar_ataque(self, ataque: Ataque, alvo: "Monstrinho") -> str:
        """[POLIMORFISMO] Sobrescreve para ativar habilidade passiva de regeneração."""
        resultado = super().usar_ataque(ataque, alvo)
        # Recupera PE se causou dano (detectado por "de dano" no log)
        if "de dano" in resultado:
            ganho = min(5, self.pe_max - self.pe_atual)
            self.pe_atual += ganho
            if ganho > 0:
                resultado += f"\n💚 Fissão: recuperou {ganho} PE!"
        return resultado

    def habilidade_passiva_descricao(self) -> str:
        return "💚 Fissão: recupera 5 PE sempre que causar dano."


class Fungo(Monstrinho):
    """
    [HERANÇA] Fungos são lentos mas muito resistentes.
    Habilidade passiva: Quitina — reduz todo dano recebido em 3 pontos
    adicionais (empilha com a defesa normal).
    """

    def __init__(self, nome, hp_max, defesa, velocidade, ataques):
        super().__init__(nome, "Fungo", hp_max, defesa, velocidade, ataques)

    def reducao_defesa(self) -> int:
        """[POLIMORFISMO] Fungos têm redução de defesa maior (base + 3 flat)."""
        return (self.defesa // 2) + 3

    def habilidade_passiva_descricao(self) -> str:
        return "🍄 Quitina: reduz todo dano recebido em +3 pontos extras."


# ──────────────────────────────────────────────────────────────
#  CATÁLOGO DE MONSTRINHOS
# ──────────────────────────────────────────────────────────────

atks_virus = [
    Ataque("Lise Celular",     25, 15),
    Ataque("Mutação Genética", 15,  8),
    Ataque("Injeção de RNA",   18, 10),
    Ataque("Carga Viral",      30, 22),
]
atks_bacteria = [
    Ataque("Toxina Bacteriana", 22, 12),
    Ataque("Fissão Binária",    14,  8),
    Ataque("Biofilme Protetor", 18, 10),
    Ataque("Super Infecção",    32, 25),
]
atks_fungo = [
    Ataque("Chuva de Esporos",  20, 10),
    Ataque("Micose Profunda",   26, 16),
    Ataque("Decomposição",      15,  7),
    Ataque("Brotamento Brutal", 35, 24),
]

CATALOGO: list[Monstrinho] = [
    # ── Vírus (mais rápidos, menos HP) ──────────────────────
    Virus("SARS-CoV-2", hp_max=90,  defesa=10, velocidade=35, ataques=atks_virus),
    Virus("H1N1",        hp_max=95,  defesa=12, velocidade=30, ataques=atks_virus),
    Virus("HIV",         hp_max=100, defesa=8,  velocidade=40, ataques=atks_virus),

    # ── Bactérias (equilibradas) ─────────────────────────────
    Bacteria("KPC (Superbactéria)", hp_max=120, defesa=18, velocidade=15, ataques=atks_bacteria),
    Bacteria("Salmonella",           hp_max=105, defesa=14, velocidade=22, ataques=atks_bacteria),
    Bacteria("Lactobacillus",        hp_max=125, defesa=12, velocidade=20, ataques=atks_bacteria),

    # ── Fungos (lentos, muita defesa/vida) ───────────────────
    Fungo("Candida auris",    hp_max=115, defesa=16, velocidade=12, ataques=atks_fungo),
    Fungo("Cogumelo Proibido",hp_max=110, defesa=18, velocidade=10, ataques=atks_fungo),
    Fungo("Penicillium",      hp_max=120, defesa=14, velocidade=14, ataques=atks_fungo),
]


# ==============================================================
#  INTERFACE GRÁFICA  —  Tkinter
# ==============================================================

CORES = {
    "bg":        "#1a1a2e",   # fundo escuro (científico/misterioso)
    "painel":    "#16213e",
    "accent":    "#0f3460",
    "Vírus":     "#e94560",   # vermelho
    "Bactéria":  "#4ecca3",   # verde-água
    "Fungo":     "#f5a623",   # laranja
    "texto":     "#eaeaea",
    "log_bg":    "#0d0d1a",
    "log_fg":    "#a8d8a8",
    "btn_bg":    "#0f3460",
    "btn_hover": "#e94560",
    "desistir":  "#444",
}

def cor_tipo(tipo: str) -> str:
    return CORES.get(tipo, CORES["texto"])


class JogoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("⚗️ BioMonsters Arena")
        self.root.geometry("600x640")
        self.root.configure(bg=CORES["bg"])
        self.root.resizable(False, False)

        self.monstro_jogador: Monstrinho | None = None
        self.monstro_inimigo: Monstrinho | None = None
        self.botoes_ataque: list[tk.Button] = []

        self.tela_selecao()

    # ── Utilitários de tela ──────────────────────────────────

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.botoes_ataque.clear()

    def _btn(self, parent, texto, comando, largura=18, altura=2,
             bg=None, fg=None, fonte=("Courier", 9, "bold")):
        bg = bg or CORES["btn_bg"]
        fg = fg or CORES["texto"]
        b = tk.Button(
            parent, text=texto, command=comando,
            width=largura, height=altura, font=fonte,
            bg=bg, fg=fg, activebackground=CORES["btn_hover"],
            activeforeground="white", relief="flat", cursor="hand2",
            bd=0, highlightthickness=0
        )
        return b

    # ── Tela de Seleção ──────────────────────────────────────

    def tela_selecao(self):
        self.limpar_tela()

        tk.Label(
            self.root,
            text="⚗️  BioMonsters Arena",
            font=("Courier", 18, "bold"),
            bg=CORES["bg"], fg=CORES["texto"]
        ).pack(pady=(20, 4))

        tk.Label(
            self.root,
            text="Escolha seu Bio-Monster para a batalha!",
            font=("Courier", 10),
            bg=CORES["bg"], fg="#888"
        ).pack(pady=(0, 14))

        for tipo in ["Vírus", "Bactéria", "Fungo"]:
            frame_tipo = tk.LabelFrame(
                self.root,
                text=f"  {tipo}  ",
                font=("Courier", 10, "bold"),
                bg=CORES["painel"], fg=cor_tipo(tipo),
                bd=1, relief="groove", padx=8, pady=6
            )
            frame_tipo.pack(fill="x", padx=22, pady=5)

            monstros = [m for m in CATALOGO if m.tipo == tipo]
            for m in monstros:
                passiva = m.habilidade_passiva_descricao()
                texto_btn = (
                    f"{m.nome}\n"
                    f"HP:{m.hp_max}  DEF:{m.defesa}  VEL:{m.velocidade}"
                )
                btn = self._btn(
                    frame_tipo, texto_btn,
                    lambda mo=m: self.iniciar_batalha(mo),
                    largura=19, altura=2,
                    bg=CORES["accent"], fg=cor_tipo(tipo)
                )
                btn.pack(side=tk.LEFT, padx=6, pady=4)

                # Tooltip simples com habilidade passiva
                self._adicionar_tooltip(btn, passiva)

    def _adicionar_tooltip(self, widget: tk.Widget, texto: str):
        """Exibe um tooltip ao passar o mouse sobre o widget."""
        tip = None

        def entrar(event):
            nonlocal tip
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 4
            tip = tk.Toplevel(widget)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{x}+{y}")
            tk.Label(
                tip, text=texto, font=("Courier", 8),
                bg="#222", fg="#ddd", relief="flat", padx=6, pady=3
            ).pack()

        def sair(event):
            nonlocal tip
            if tip:
                tip.destroy()
                tip = None

        widget.bind("<Enter>", entrar)
        widget.bind("<Leave>", sair)

    # ── Iniciar Batalha ──────────────────────────────────────

    def iniciar_batalha(self, monstro_escolhido: Monstrinho):
        self.monstro_jogador = monstro_escolhido.clonar()
        # Inimigo não pode ser o mesmo que o jogador escolheu
        possiveis = [m for m in CATALOGO if m.nome != monstro_escolhido.nome]
        self.monstro_inimigo = random.choice(possiveis).clonar()
        self.montar_tela_batalha()

    # ── Tela de Batalha ──────────────────────────────────────

    def montar_tela_batalha(self):
        self.limpar_tela()

        # Cabeçalho
        tk.Label(
            self.root, text="⚔️  Batalha!",
            font=("Courier", 14, "bold"),
            bg=CORES["bg"], fg=CORES["texto"]
        ).pack(pady=(14, 2))

        # Status do inimigo
        self.lbl_inimigo = tk.Label(
            self.root, font=("Courier", 11, "bold"),
            bg=CORES["bg"], fg=cor_tipo(self.monstro_inimigo.tipo)
        )
        self.lbl_inimigo.pack()

        # Barra de HP inimigo
        self.frame_hp_inimigo = tk.Frame(self.root, bg=CORES["bg"])
        self.frame_hp_inimigo.pack()
        self.canvas_hp_inimigo = tk.Canvas(
            self.frame_hp_inimigo, width=340, height=12,
            bg="#333", highlightthickness=0
        )
        self.canvas_hp_inimigo.pack(pady=2)

        tk.Label(
            self.root, text="— VS —",
            font=("Courier", 12, "bold"),
            bg=CORES["bg"], fg="#555"
        ).pack(pady=4)

        # Status do jogador
        self.lbl_jogador = tk.Label(
            self.root, font=("Courier", 11, "bold"),
            bg=CORES["bg"], fg=cor_tipo(self.monstro_jogador.tipo)
        )
        self.lbl_jogador.pack()

        # Barra de HP jogador
        self.frame_hp_jogador = tk.Frame(self.root, bg=CORES["bg"])
        self.frame_hp_jogador.pack()
        self.canvas_hp_jogador = tk.Canvas(
            self.frame_hp_jogador, width=340, height=12,
            bg="#333", highlightthickness=0
        )
        self.canvas_hp_jogador.pack(pady=2)

        # Log de batalha
        self.txt_log = tk.Text(
            self.root, height=8, width=62,
            state="disabled", wrap="word",
            bg=CORES["log_bg"], fg=CORES["log_fg"],
            font=("Courier", 9), relief="flat",
            padx=8, pady=6
        )
        self.txt_log.pack(pady=8, padx=16)

        # Botões de ataque (grid 2×2)
        self.frame_botoes = tk.Frame(self.root, bg=CORES["bg"])
        self.frame_botoes.pack()

        for i, atk in enumerate(self.monstro_jogador.ataques):
            btn = self._btn(
                self.frame_botoes,
                f"{atk.nome}\n({atk.custo_pe} PE)",
                lambda a=atk: self.processar_rodada(a),
                largura=20, altura=2
            )
            btn.grid(row=i // 2, column=i % 2, padx=6, pady=4)
            self.botoes_ataque.append(btn)

        # Botão desistir
        self._btn(
            self.root, "↩  Desistir e voltar",
            self.tela_selecao,
            largura=22, altura=1,
            bg=CORES["desistir"], fg="#aaa",
            fonte=("Courier", 8)
        ).pack(pady=(4, 10))

        self.atualizar_telas()
        self.log(
            f"A batalha começou!\n"
            f"{self.monstro_jogador.nome} (VEL:{self.monstro_jogador.velocidade}) "
            f"enfrenta {self.monstro_inimigo.nome} (VEL:{self.monstro_inimigo.velocidade})!\n"
            f"Passiva do seu monstrinho → {self.monstro_jogador.habilidade_passiva_descricao()}"
        )

    def _desenhar_barra_hp(self, canvas: tk.Canvas, monstrinho: Monstrinho, cor: str):
        canvas.delete("all")
        proporcao = monstrinho.hp_atual / monstrinho.hp_max
        largura_total = 340
        largura_hp = int(largura_total * proporcao)
        canvas.create_rectangle(0, 0, largura_hp, 12, fill=cor, outline="")

    def atualizar_telas(self):
        j = self.monstro_jogador
        i = self.monstro_inimigo

        self.lbl_inimigo.config(
            text=(f"👾 {i.nome} [{i.tipo}]\n"
                  f"HP: {i.hp_atual}/{i.hp_max}")
        )
        self.lbl_jogador.config(
            text=(f"🦸 {j.nome} [{j.tipo}]\n"
                  f"HP: {j.hp_atual}/{j.hp_max}  |  PE: {j.pe_atual}/{j.pe_max}")
        )
        self._desenhar_barra_hp(self.canvas_hp_inimigo, i, cor_tipo(i.tipo))
        self._desenhar_barra_hp(self.canvas_hp_jogador, j, cor_tipo(j.tipo))

    def alterar_estado_botoes(self, estado: str):
        for btn in self.botoes_ataque:
            btn.config(state=estado)

    def log(self, mensagem: str):
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, mensagem + "\n" + "─" * 48 + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    # ── Lógica de combate ────────────────────────────────────

    def checar_fim_de_jogo(self) -> bool:
        if not self.monstro_inimigo.esta_vivo():
            self.log("🏆 VOCÊ VENCEU! O inimigo foi derrotado!")
            messagebox.showinfo("Fim da Batalha", "🏆 Você venceu!")
            self.tela_selecao()
            return True
        if not self.monstro_jogador.esta_vivo():
            self.log("💀 VOCÊ PERDEU! Seu monstrinho foi derrotado...")
            messagebox.showerror("Fim da Batalha", "💀 Você perdeu...")
            self.tela_selecao()
            return True
        return False

    def processar_rodada(self, ataque_escolhido: Ataque):
        self.alterar_estado_botoes("disabled")
        ataque_inimigo = random.choice(self.monstro_inimigo.ataques)

        if self.monstro_jogador.velocidade >= self.monstro_inimigo.velocidade:
            # Jogador ataca primeiro
            self.executar_ataque_jogador(ataque_escolhido)
            if not self.checar_fim_de_jogo():
                self.root.after(1200, lambda: self.executar_ataque_inimigo(ataque_inimigo))
        else:
            # Inimigo é mais rápido
            self.log(f"⚡ {self.monstro_inimigo.nome} é mais rápido e ataca primeiro!")
            self.executar_ataque_inimigo(ataque_inimigo)
            if not self.checar_fim_de_jogo():
                self.root.after(1200, lambda: self.executar_ataque_jogador(ataque_escolhido))

    def executar_ataque_jogador(self, ataque: Ataque):
        resultado = self.monstro_jogador.usar_ataque(ataque, self.monstro_inimigo)
        self.log(resultado)
        self.atualizar_telas()

    def executar_ataque_inimigo(self, ataque: Ataque):
        resultado = self.monstro_inimigo.usar_ataque(ataque, self.monstro_jogador)
        self.log(resultado)
        self.atualizar_telas()
        if not self.checar_fim_de_jogo():
            self.alterar_estado_botoes("normal")


# ==============================================================
#  PONTO DE ENTRADA
# ==============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoApp(root)
    root.mainloop()

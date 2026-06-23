
# Project Title

A brief description of what this project does and who it's for

# ⚗️ BioMonsters Arena

Jogo de batalha por turnos desenvolvido em Python com Tkinter, criado como projeto final da disciplina de Programação II.

Inspirado em jogos como Pokémon e Monster Hunter, o jogador escolhe um micro-organismo e o leva para batalhar contra inimigos controlados pela IA.

---

## 🎮 Como Jogar

1. Execute o arquivo `biomonsters.py` com Python 3.x
2. Escolha seu Bio-Monster na tela de seleção (passe o mouse sobre eles para ver a habilidade passiva!)
3. Durante a batalha, escolha um dos 4 ataques disponíveis a cada turno
4. Derrote o inimigo antes que seu HP chegue a zero

---

## 🧬 Tipos e Vantagens

O jogo possui um triângulo de vantagens de tipos, similar ao Pokémon

 Tipo  Vence contra  Perde para 
-------------------------------
 🔴 Vírus  Bactéria  Fungo 
 🟢 Bactéria  Fungo  Vírus 
 🟠 Fungo  Vírus  Bactéria 

Ataques com vantagem causam +50% de dano (×1.5).  
Ataques com desvantagem causam −50% de dano (×0.5).

---

## 🦠 Bio-Monsters Disponíveis

### 🔴 Vírus — Rápidos e agressivos
 Nome  HP  Defesa  Velocidade 
------------------------------
 HIV  100  8  40 
 SARS-CoV-2  90  10  35 
 H1N1  95  12  30 

 🧬 Habilidade Passiva — Mutação 20% de chance de acerto crítico (+35% de dano).

### 🟢 Bactérias — Equilibradas e resistentes
 Nome  HP  Defesa  Velocidade 
------------------------------
 Lactobacillus  125  12  20 
 KPC (Superbactéria)  120  18  15 
 Salmonella  105  14  22 

 💚 Habilidade Passiva — Fissão Recupera 5 PE sempre que causar dano.

### 🟠 Fungos — Lentos, mas extremamente resistentes
 Nome  HP  Defesa  Velocidade 
------------------------------
 Penicillium  120  14  14 
 Candida auris  115  16  12 
 Cogumelo Proibido  110  18  10 

 🍄 Habilidade Passiva — Quitina Reduz todo dano recebido em +3 pontos extras além da defesa normal.

---

## 💻 Tecnologias e Conceitos

- Python 3.x
- Tkinter — interface gráfica
- Programação Orientada a Objetos
  - Encapsulamento — atributos e métodos organizados dentro de cada classe
  - Herança — `Virus`, `Bacteria` e `Fungo` herdam da classe base `Monstrinho`
  - Polimorfismo — cada subclasse sobrescreve métodos como `bonus_ataque()`, `reducao_defesa()` e `habilidade_passiva_descricao()`

---

## 📁 Estrutura do Projeto

```
biomonsters
│
├── biomonsters.py   # Código principal (lógica + interface)
└── README.md        # Este arquivo
```

---

## ▶️ Requisitos

- Python 3.10 ou superior
- Biblioteca `tkinter` (já incluída na instalação padrão do Python)

Para executar
```bash
python biomonsters.py
```

---

Projeto desenvolvido para a disciplina de Programação II.
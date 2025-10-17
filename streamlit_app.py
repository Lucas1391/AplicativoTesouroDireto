import random
import streamlit as st

# Função para o nível 1
def nivel_1():
    minha_lista = ["tirar blusa", "tirar short", "tirar sutiã", "tirar calcinha","Três tapinhas no Bumbum","Caricia na pinta ou pipiu"]
    valor_aleatorio = random.choice(minha_lista)
    st.write(f"Opção sorteada: {valor_aleatorio}")

# Função para o nível 2
def nivel_2():
    minha_lista2 = ["Beijo de língua", "Beijo no peito", "Passar peito ou pinta no corpo", "Beijo rapidinho no pipiu ou pinta"]
    valor_aleatorio = random.choice(minha_lista2)
    st.write(f"Opção sorteada: {valor_aleatorio}")

# Interface do usuário com Streamlit
st.title("Jogo de Sorteio")

# Solicitar nível do usuário
nivel = st.selectbox("Selecione seu nível de Jogo:", (1, 2))

# Botão para sortear
if st.button("Sortear"):
    if nivel == 1:
        nivel_1()
    elif nivel == 2:
        nivel_2()
    else:
        st.write("Nível inválido! Selecione 1 ou 2.")
        

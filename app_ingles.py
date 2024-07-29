import json

import requests
import streamlit as st
from translate import Translator


# Função para obter uma citação aleatória
def get_random_text():
    try:
        response = requests.get(
            'https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json'
        )
        response.raise_for_status()
        quote_data = json.loads(response.text)
        return quote_data['quoteText']
    except requests.exceptions.RequestException as e:
        st.error(f'Erro ao buscar texto aleatório: {e}')
        return 'Aguarde 1 minuto para nova solicitação!'
    except ValueError as e:
        st.error(f'Erro ao processar a resposta: {e}')
        return 'Aguarde 1 minuto para nova solicitação!'


# Função para traduzir o texto
def translate_text(text, target_language):
    if target_language == 'Selecione o idioma':
        return 'Por favor, selecione um idioma'
    else:
        translator = Translator(to_lang=target_language)
        return translator.translate(text)


# Configuração da página
st.set_page_config(
    page_title='Treinando Inglês',
    page_icon='📚',
    layout='centered',
    initial_sidebar_state='collapsed',
)

# Título do aplicativo
st.title('Treinando Inglês')
st.write(
    """<p style="font-size: 14px;
        font-style: italic;">
        Pratique seu inglês traduzindo citações aleatórias!</p>""",
    unsafe_allow_html=True,
)

# Estado inicial da citação e da tradução
if 'random_text' not in st.session_state:
    st.session_state.random_text = get_random_text()
if 'translation_input' not in st.session_state:
    st.session_state.translation_input = ''

# Exibir a citação aleatória
st.markdown(
    f'<h3><em>{st.session_state.random_text}</em></h3>', unsafe_allow_html=True
)

# Botão para atualizar a citação
if st.button('Atualizar Citação'):
    st.session_state.random_text = get_random_text()
    st.session_state.translation_input = ''
    st.rerun()

# Entrada de tradução do usuário
translation_input = st.text_area(
    'Digite sua tradução aqui e compare com a tradução:',
    value=st.session_state.translation_input,
    height=100,
    key='translation_input',
).strip()

# Spinner de seleção de idioma
language = st.selectbox(
    'Selecione o idioma:',
    ('pt-br', 'fr', 'de', 'it', 'es'),
)

# Botão de tradução
if st.button('Traduzir'):
    translated_text = translate_text(st.session_state.random_text, language)
    st.write(f'Tradução: {translated_text}')

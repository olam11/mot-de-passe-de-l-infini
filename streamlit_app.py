import streamlit as st

@st.cache_data
def config():
    st.set_page_config(page_title="mot de passe de l'infini",page_icon=":infinity:")
    
    

config()
if 'key' not in st.session_state:
    st.session_state.running = 0
st.session_state.running = st.session_state.running+1
st.write(st.session_state.running)
st.button("rerun")
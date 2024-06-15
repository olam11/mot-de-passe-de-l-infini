import streamlit as st

st.set_page_config(page_title="mot de passe de l'infini",page_icon=":infinity:")
    
if 'running' not in st.session_state:
    st.session_state.running = 0
    
st.session_state.running = st.session_state.running+1
st.write(st.session_state.running)
st.write("coucou")
st.button("rerun")
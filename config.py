import os
try:
    import streamlit as st
except Exception:
    st = None

def load_secrets():
    if st is None:
        return
    for key in ["OPENAI_API_KEY","OPENAI_MODEL","SUPABASE_URL","SUPABASE_KEY"]:
        if not os.getenv(key):
            try:
                value = st.secrets.get(key)
            except Exception:
                value = None
            if value:
                os.environ[key] = str(value)

load_secrets()

import streamlit as st
from PIL import Image

from partials.report import report
from partials.report_local import report_local

def main():
    favicon = Image.open('files/logo.webp')
    st.set_page_config(
        page_title='Relatório de Extrato',
        page_icon=favicon,
        layout="wide"
    )

    st.header('Relatório de Extrato NuBank')
    st.caption('by. Josué Santos')

    report()
    
if __name__ == '__main__':
    main()

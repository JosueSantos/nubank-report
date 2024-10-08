# -*- coding: utf-8 -*-
import streamlit as st
from services.FilesService import FilesService
from services.ReportService import ReportService
from io import StringIO
import pandas as pd


def report():
    st.markdown('### &#x25A3; Análise de Gastos por Mês')
    
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    if uploaded_file is not None:
        string_data = uploaded_file.getvalue().decode("utf-8")
        data = StringIO(string_data)
        
        df = pd.read_csv(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['category'] != 'payment']
        df = df.sort_values(by='date')

        total_month, value_installments, percentMonthSubInstallments, maxTitleSum, percentMonthSubInstallmentsInTitle, totalMov, maxTitle, maxTitleCount, movDaily, filtered_df, result_df = ReportService.buildInfo(df)
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(
            label="Total ",
            value=ReportService.format_money(total_month)
        )

        kpi2.metric(
            label="Parcelamentos",
            value=ReportService.format_money(value_installments)
        )

        kpi3.metric(
            label="Percentual de Comprometimento",
            value="{:.2f}%".format(percentMonthSubInstallments)
        )

        kpi1.metric(
            label="Movimentações " + maxTitle,
            value=maxTitleCount
        )

        kpi2.metric(
            label= "Soma dos valores do " + maxTitle,
            value=ReportService.format_money(maxTitleSum)
        )

        kpi3.metric(
            label="Percentual de Comprometimento",
            value="{:.2f}%".format(percentMonthSubInstallmentsInTitle)
        )

        kpi1.metric(
            label= "Total de Movimentações",
            value=totalMov
        )

        kpi2.metric(
            label="Movimentações por Dia",
            value="{:.2f}".format(movDaily)
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Compras Recorrentes")
            st.dataframe(result_df)
        with col2:
            st.markdown('##### Dados Carregados:')
            st.write(filtered_df)
        
    
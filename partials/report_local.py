# -*- coding: utf-8 -*-
import streamlit as st
from services.FilesService import FilesService
from services.ReportService import ReportService


def report_local():
    st.markdown('### &#x25A3; Análise de Gastos por Mês')
    
    data = FilesService.load_and_process_data('files')

    option_month_ref = st.selectbox('Selecione um mês:', data['month_ref'].sort_values(ascending=False).unique())

    total_month, value_installments, percentMonthSubInstallments, maxTitleSum, percentMonthSubInstallmentsInTitle, totalMov, maxTitle, maxTitleCount, movDaily, filtered_df, result_df = ReportService.buildInfoLocal(option_month_ref, data)
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(
        label="Total " + option_month_ref,
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
    
    
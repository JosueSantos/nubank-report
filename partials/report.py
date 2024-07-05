# -*- coding: utf-8 -*-
import streamlit as st
from services.FilesService import FilesService
from services.ReportService import ReportService


def report():
    st.markdown('### &#x25A3; Análise de Gastos por Mês')
    
    data = FilesService.load_and_process_data('files')

    option_month_ref = st.selectbox('Selecione um mês:', data['month_ref'].sort_values(ascending=False).unique())

    total_month, value_installments, percentMonthSubInstallments, totalMonthSubInstallments, maxTitleSum, percentMonthSubInstallmentsInTitle, totalMonthSubInstallmentsInTitle, totalMov, maxTitle, maxTitleCount, movDiff, movDaily, filtered_df, result_df = ReportService.buildInfo(option_month_ref, data)
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
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

    kpi4.metric(
        label="Total - Parcelamentos",
        value=ReportService.format_money(totalMonthSubInstallments)
    )

    kpi2.metric(
        label= maxTitle,
        value=ReportService.format_money(maxTitleSum)
    )

    kpi3.metric(
        label="Percentual de Comprometimento",
        value="{:.2f}%".format(percentMonthSubInstallmentsInTitle)
    )

    kpi4.metric(
        label="Total - " + maxTitle,
        value=ReportService.format_money(totalMonthSubInstallmentsInTitle)
    )

    kpi2.metric(
        label= "Total de Movimentações",
        value=totalMov
    )

    kpi3.metric(
        label="Movimentações " + maxTitle,
        value=maxTitleCount
    )

    kpi4.metric(
        label="Diferentes Movimentações",
        value=movDiff
    )

    kpi4.metric(
        label="Movimentações por Dia",
        value="{:.2f}".format(movDaily)
    )

    st.markdown("##### Compras Recorrentes")
    st.dataframe(result_df)
    
    st.markdown('##### Dados Carregados:')
    st.write(filtered_df)
    
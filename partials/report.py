# -*- coding: utf-8 -*-
import streamlit as st
from services.FilesService import FilesService
import pandas as pd
import locale
import re


def format_money(value):
    return locale.currency(value, grouping=True)

def count_installments(title):
    matches = re.findall(r'\d+/\d+', title)
    return len(matches)

def report():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    st.markdown('### &#x25A3; Análise de Gastos por Mês')
    
    data = FilesService.load_and_process_data('files')

    option_month_ref = st.selectbox('Selecione um mês:', data['month_ref'].sort_values(ascending=False).unique())

    filtered_df = data[data['month_ref'] == option_month_ref]

    total_month = data[data['month_ref'] == option_month_ref]['amount'].sum()

    title_installments = filtered_df['title'].apply(count_installments)
    title_installments = title_installments[title_installments != 0]
    title_installments = filtered_df.loc[title_installments.index]
    
    value_installments = title_installments['amount'].sum()
    size_installments = title_installments['amount'].count()


    title_counts = filtered_df['title'].value_counts().head(5)
    title_sums = filtered_df.groupby('title')['amount'].sum().loc[title_counts.index]
    title_count = filtered_df.groupby('title')['amount'].count().loc[title_counts.index]
    title_sums_formatted = title_sums.apply(format_money)

    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(
        label="Total " + option_month_ref,
        value=format_money(total_month)
    )

    kpi2.metric(
        label="Parcelamentos",
        value=format_money(value_installments)
    )

    kpi3.metric(
        label="Percentual de Comprometimento",
        value="{:.2f}%".format(value_installments / total_month * 100)
    )

    kpi4.metric(
        label="Total - Parcelamentos",
        value=format_money(total_month - value_installments)
    )

    kpi2.metric(
        label= title_counts.index[0],
        value=format_money(title_sums[0])
    )

    kpi3.metric(
        label="Percentual de Comprometimento",
        value="{:.2f}%".format((title_sums[0] + value_installments) / total_month * 100)
    )

    kpi4.metric(
        label="Total - " + title_counts.index[0],
        value=format_money(total_month - title_sums[0] - value_installments)
    )

    kpi2.metric(
        label= "Total de Movimentações",
        value=filtered_df['amount'].count() - size_installments
    )

    kpi3.metric(
        label="Movimentações " + title_counts.index[0],
        value=title_count[0]
    )

    kpi4.metric(
        label="Diferentes Movimentações",
        value=filtered_df['amount'].count() - title_count[0] - size_installments
    )

    kpi4.metric(
        label="Movimentações por Dia",
        value="{:.2f}".format((filtered_df['amount'].count() - title_count[0] - size_installments) / 30)
    )

    result_df = pd.DataFrame({
        'Title': title_counts.index,
        'Number of Occurrences': title_counts.values,
        'Total Amount': title_sums_formatted.values
    })

    st.markdown("##### Compras Recorrentes")
    st.dataframe(result_df)
    
    st.markdown('##### Dados Carregados:')
    st.write(filtered_df)
    
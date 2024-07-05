# nubank-report
- Acesse o https://app.nubank.com.br/
- Exporte os Extratos no formato CSV
- Adicione-os a pasta /files

- Instale dependencias com `pip install -r requirements.txt`
- Execute a aplicação `streamlit run app.py`

O sistema identifica no extrado:
- O valor da fatura do mês
- A soma dos parcelamentos
- O percentual do valor da Fatura comprometido pelos parcelamentos
- As 5 compras recorrentes com maior frêquencia
- A Soma das compras com maior recorrência
- O percentual de comprometimento da fatura, pelos parcelamentos e pela soma das compras mais recorrentes
- O total de movimentações na fatura, subtraindo os parcelamentos
- O total de movimentações da compra com maior recorrencia
- O total de movimentações subtraindo os parcelamentos e a compra com maior recorrencia
- A média de compras por dia

### Print

![image](/files/reportNu.PNG)

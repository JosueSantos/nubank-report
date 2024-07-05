import locale
import re
import pandas as pd


class ReportService():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    def format_money(value):
        return locale.currency(value, grouping=True)

    def count_installments(title):
        matches = re.findall(r'\d+/\d+', title)
        return len(matches)
    
    def buildInfo(option_month_ref, data):
        filtered_df = data[data['month_ref'] == option_month_ref]
    
        title_installments = filtered_df['title'].apply(ReportService.count_installments)
        title_installments = title_installments[title_installments != 0]
        title_installments = filtered_df.loc[title_installments.index]
        
        size_installments = title_installments['amount'].count()

        title_counts = filtered_df['title'].value_counts()
        title_sums = filtered_df.groupby('title')['amount'].sum().loc[title_counts.index]
        title_count = filtered_df.groupby('title')['amount'].count().loc[title_counts.index]
        title_sums_formatted = title_sums.apply(ReportService.format_money)

        result_df = pd.DataFrame({
            'Title': title_counts.index,
            'Number of Occurrences': title_counts.values,
            'Total Amount': title_sums_formatted.values
        })
        
        total_month = data[data['month_ref'] == option_month_ref]['amount'].sum()
        value_installments = title_installments['amount'].sum()
        percentMonthSubInstallments = value_installments / total_month * 100
        maxTitleSum = title_sums[0]
        percentMonthSubInstallmentsInTitle = (title_sums[0] + value_installments) / total_month * 100
        totalMov = filtered_df['amount'].count() - size_installments
        maxTitle = title_counts.index[0]
        maxTitleCount = title_count[0]
        movDaily = (filtered_df['amount'].count() - size_installments) / 30

        return total_month, value_installments, percentMonthSubInstallments, maxTitleSum, percentMonthSubInstallmentsInTitle, totalMov, maxTitle, maxTitleCount, movDaily, filtered_df, result_df
    
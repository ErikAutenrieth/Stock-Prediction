import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

from charts import line_chart

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from ml.database.influxdb_manager import InfluxDBOperations

db = InfluxDBOperations()


def main():
    st.markdown("<h3 style='text-align: center; color: black;'>Stock Price (15-day-ahead) Trend Prediction</h3>",
                unsafe_allow_html=True)

    stock_symbol = ["^GSPC", "S&P500"]

    end_date = datetime.now()
    start_date = end_date - relativedelta(months=6)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    data = yf.download(stock_symbol[0], start=start_date, end=end_date)

    if not data.empty:
        predictions = db.get_prediction_from_influx()

        # Kerzenchart erstellen
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])

        for index, row in predictions.iterrows():
            date = row['Date']
            target = row['Target']
            if date in data.index:
                fig.add_annotation(
                    x=date,
                    y=data.loc[date, 'Close'],
                    text='↑' if target == 1 else '↓',
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='green' if target == 1 else 'red'
                )

        fig.update_layout(
            title=f'Stock Prediction for {stock_symbol[1]}',
            xaxis_rangeslider_visible=False,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label='1M', step='month', stepmode='backward'),
                        dict(count=3, label='3M', step='month', stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                type='date'
            ),
            xaxis_tickformat='%Y-%m-%d'
        )
        st.plotly_chart(fig)

        line_chart_plot = line_chart(predictions, stock_symbol[0])

        st.plotly_chart(line_chart_plot)

        model_info = predictions.drop("time", axis=1).drop_duplicates()
        model_info['Date'] = pd.to_datetime(model_info['Date']).dt.strftime('%Y-%m-%d')
        st.write("Model Information and Accuracy")
        st.table(model_info)

    else:
        st.write('No data available.')


if __name__ == '__main__':
    main()

# %%

# %%

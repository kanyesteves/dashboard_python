import pandas as pd
import streamlit as st
import plotly.express as px

#Setar tamanho da tabela a ser apresentada
st.set_page_config(layout="wide")

#Ler arquivo .csv
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

#Tratar coluna Data para usar nos filtros dos gráficos
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

#Seta as posições das colunas
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

#Gráfico 1 - Faturamento por dia.
fig_date = px.bar(df_filtered, x="Date", y="Total",
                  color="City",
                  title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

#Gráfico 2 - Faturamento por tipo do produto.
fig_prod = px.bar(df_filtered, x="Date", y="Product line",
                  color="City",
                  title="Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

#Gráfico 3 - Faturamento de cada filial.
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                  color="City",
                  title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

#Gráfico 4 - Faturamento por tipo de pagamento.
fig_city = px.pie(df_filtered, values="Total", names="Payment",
                  title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_city, use_container_width=True)

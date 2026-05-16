import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
import plotly.express as px
st.set_page_config(page_title="AI销售数据分析助手")

st.title("AI销售数据分析助手")

st.write("上传销售数据，自动生成AI分析报告")

uploaded_file = st.file_uploader(
    "上传销售数据文件",
    type=["xlsx", "csv"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("销售数据预览")

    st.dataframe(df)
    st.subheader("销售数据分析")

    total_sales = df["销售额"].sum()

    avg_sales = df["销售额"].mean()

    top_product = (
        df.groupby("产品")["销售额"]
        .sum()
        .idxmax()
    )

    st.metric("总销售额", f"¥{total_sales:,.0f}")

    st.metric("平均销售额", f"¥{avg_sales:,.0f}")

    st.metric("销量最高产品", top_product)   

    st.subheader("产品销售排行")

    product_sales = (
        df.groupby("产品")["销售额"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        product_sales,
        x="产品",
        y="销售额",
        title="产品销售额排行"
    )

    st.plotly_chart(fig)
    st.subheader("AI销售分析报告")

    data_summary = product_sales.to_string(index=False)

    prompt = f"""
    你是一名销售数据分析师。

    请根据以下销售数据，
    生成一份简洁专业的销售分析报告。

    数据如下：

    {data_summary}
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    ai_result = response.choices[0].message.content

    st.write(ai_result)
        
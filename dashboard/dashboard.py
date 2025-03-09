import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """Load dataset"""
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['year'] = df['order_purchase_timestamp'].dt.year
    return df

def plot_trend_orders(df):
    """Plot tren jumlah pesanan dari waktu ke waktu"""
    orders_trend = df.resample('M', on='order_purchase_timestamp').size()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(orders_trend.index, orders_trend.values, marker='o', linestyle='-')
    ax.set_title("Tren Jumlah Pesanan")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Jumlah Pesanan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_top_categories(df):
    """Plot top 10 kategori produk populer"""
    top_categories = df['product_category_name_english'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax, palette="magma")
    ax.set_title("Top 10 Kategori Produk Populer")
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)

def plot_payment_distribution(df):
    """Plot metode pembayaran populer"""
    payment_counts = df['payment_type'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax, palette="coolwarm")
    ax.set_title("Distribusi Metode Pembayaran")
    ax.set_xlabel("Metode Pembayaran")
    ax.set_ylabel("Jumlah Penggunaan")
    st.pyplot(fig)

def rfm_analysis(df):
    latest_date = df['order_purchase_timestamp'].max()
    rfm_df = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (latest_date - x.max()).days,  # Recency
        'order_id': 'nunique',  # Frequency
        'price': 'sum'  # Monetary
    })
    rfm_df.columns = ['Recency', 'Frequency', 'Monetary']
    return rfm_df

def plot_rfm_visualization(rfm_df):
    """Visualisasi RFM Analysis"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    sns.histplot(rfm_df['Recency'], bins=20, kde=True, ax=axes[0], color='blue')
    axes[0].set_title("Distribusi Recency")
    
    sns.histplot(rfm_df['Frequency'], bins=20, kde=True, ax=axes[1], color='green')
    axes[1].set_title("Distribusi Frequency")
    
    sns.histplot(rfm_df['Monetary'], bins=20, kde=True, ax=axes[2], color='red')
    axes[2].set_title("Distribusi Monetary")
    
    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("📊Dashboard E-commerce Public Dataset Analysis")
    df = load_data()

    # Metrics
    total_orders = df.shape[0]
    total_customers = df['customer_unique_id'].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Total Customers", f"{total_customers:,}")
    
    # Filter tahun dan Logo
    st.sidebar.image("logo ecommerce.jpg")
    st.sidebar.header("Filter")
    rfm_df = rfm_analysis(df)
    years = sorted(df['year'].unique().tolist())
    selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun"] + years)
    
    if selected_year != "Semua Tahun":
        df = df[df['year'] == selected_year]
    
    st.subheader("Tren Jumlah Pesanan")
    plot_trend_orders(df)
    st.subheader("Kategori Produk Populer")
    plot_top_categories(df)
    st.subheader("Metode Pembayaran Populer")
    plot_payment_distribution(df)
    st.subheader("RFM Analysis")
    plot_rfm_visualization(rfm_df)

if __name__ == "__main__":
    main()

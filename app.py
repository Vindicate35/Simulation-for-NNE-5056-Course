import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Sayfa ayarları
st.set_page_config(page_title="İnce Film Simülatörü", layout="centered")

st.title("İnce Film Kaplama Simülatörü")
st.markdown("Döndürerek (Spin) ve Daldırma (Dip) kaplama parametrelerinin film kalınlığına etkisini inceleyin.")

# Kullanıcı Girişleri
mod = st.radio("Kaplama Yöntemini Seçin:", ("Döndürerek Kaplama (Spin)", "Daldırma Kaplama (Dip)"))
viskozite = st.slider("Çözelti Viskozitesi (mPa.s)", 1.0, 100.0, 10.0)

# Fiziğe Dayalı Hesaplamalar ve Hız Ayarları
if mod == "Döndürerek Kaplama (Spin)":
    hiz = st.slider("Dönüş Hızı (RPM)", 1000, 8000, 3000, step=100)
    # Spin Coating Modeli: Kalınlık, hızın kareköküyle ters orantılıdır.
    kalinlik = 1500 * (viskozite / np.sqrt(hiz))
    st.success(f"**Tahmini Film Kalınlığı:** {kalinlik:.2f} nm")
    
    if hiz > 6000:
        st.warning("⚠️ Yüksek Hız Uyarısı: Hızlı buharlaşma nedeniyle 'Comet' (kuyruklu yıldız) hataları riski yüksek.")
        
else:
    hiz = st.slider("Çekme Hızı (cm/dk)", 1.0, 50.0, 10.0, step=1.0)
    # Dip Coating (Landau-Levich) Modeli: Kalınlık, (viskozite * hız) değerinin 2/3 kuvvetiyle orantılıdır.
    kalinlik = 15 * np.power((viskozite * hiz), 2/3)
    st.success(f"**Tahmini Film Kalınlığı:** {kalinlik:.2f} nm")
    
    if hiz > 35.0:
        st.warning("⚠️ Yüksek Hız Uyarısı: Kalın film birikimi 'Ribbing' (şeritlenme) ve drenaj sarkmalarına yol açabilir.")

# Dinamik Görselleştirme (Kesit)
fig = go.Figure()

# Alt Tabaka (Substrat)
fig.add_trace(go.Bar(
    x=["Kaplama Kesiti"], y=[500],
    marker_color='#7f8c8d', name='Alt Tabaka (Substrat)'
))

# İnce Film
fig.add_trace(go.Bar(
    x=["Kaplama Kesiti"], y=[kalinlik],
    marker_color='rgba(52, 152, 219, 0.8)', name='İnce Film'
))

fig.update_layout(
    barmode='stack',
    yaxis_title="Bağıl Kalınlık",
    xaxis=dict(showticklabels=False),
    height=400,
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig, use_container_width=True)

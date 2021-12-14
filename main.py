import altair as alt
import pandas as pd
import streamlit as st
import json
st.set_page_config(page_title="UAS 2021",layout='wide')
# Load Data
f = open('kode_negara_lengkap.json')
data = pd.read_csv('produksi_minyak_mentah.csv')
obj = json.load(f)
nameArr = []
regionArr = []
codeArr = []
subRegionArr = []
for item in obj :
    nameArr.append(item['name'])
    codeArr.append(item['alpha-3'])
    regionArr.append(item["region"])
    subRegionArr.append(item["sub-region"])

# Cleaning
found = False
for i, row in data.iterrows():
    found = False
    for code in codeArr :
        if row['kode_negara'] == code  :
            found = True
        if (found) :
            break
        
    if (found == False) :
        data.drop(index=i, inplace=True)

# Header
st.title("UAS IF 2112 Pemrograman Komputer 2021/2022")
st.write('Aplikasi GUI yang mengambarkan informasi seputar data produksi minyak mentah dari berbagai negara di seluruh dunia.')

# Util
def searchCode(codesearch) :
    idx = 0
    found = False
    for code in codeArr :
        if (codesearch == code and not found) :
            found = True
        if (found) :
            break
        idx += 1
    
    if (found) :
        return nameArr[idx]
    else :
        return codesearch

def searchRegion(codesearch) :
    idx = 0
    found = False
    for code in codeArr :
        if (codesearch == code and not found) :
            found = True
        if (found) :
            break
        idx += 1
    
    if (found) :
        return regionArr[idx]
    else :
        return codesearch

def searchSubRegion(codesearch) :
    idx = 0
    found = False
    for code in codeArr :
        if (codesearch == code and not found) :
            found = True
        if (found) :
            break
        idx += 1
    
    if (found) :
        return subRegionArr[idx]
    else :
        return codesearch

# Fitur Fungsi Utama
def a(name) :
    if name in nameArr :
        for item in obj :
           if (name == item['name']) :
               ccode = item['alpha-3']

        dcountry = data.loc[data['kode_negara'] == ccode]
        chart = alt.Chart(dcountry).mark_line().encode(
            x=alt.X("tahun", axis=alt.Axis(title="Tahun", format='%Y', formatType="time")),
            y=alt.Y("produksi", axis=alt.Axis(title="Jumlah Produksi"))
        ).properties(title=f'Grafik Jumlah Produksi Minyak Mentah Terhadap Waktu (Tahun) Negara {name}')
        st.altair_chart(chart, use_container_width=True)

        st.caption("Perbesar tampilan grafik dengan tombol kedua di grafik di atas")
    else :
        print("Country name is not valid.")

def b(year, idx) :
    dcountry = data.loc[data['tahun'] == year]
    dcountry = dcountry.sort_values(["produksi"], ascending=False)
    dcountry = dcountry[:idx]

    dcountry["stringname"] = dcountry["kode_negara"].apply(searchCode)             
    chart = alt.Chart(dcountry).mark_bar().encode(
        x=alt.X("stringname", axis=alt.Axis(title="Nama Negara")),
        y=alt.Y('produksi:Q', axis=alt.Axis(title="Jumlah Produksi"))
    ).properties(title=f'Grafik {idx} Negara Terbesar berdasarkan Jumlah Produksi Minyak Mentah Tahun {year} ')
    st.altair_chart(chart, use_container_width=True)
    st.caption("Perbesar tampilan grafik dengan tombol kedua di grafik di atas")

def c(idx) :
    dcountry = data
    dcountry = dcountry.drop('tahun', axis=1)
    dcountry = dcountry.groupby(['kode_negara']).sum()
    dcountry = dcountry.sort_values(["produksi"], ascending=False)
    dcountry = dcountry[:idx]
    dcountry = dcountry.reset_index(drop=False)
    dcountry["stringname"] = dcountry["kode_negara"].apply(searchCode)
    chart = alt.Chart(dcountry).mark_bar().encode(
        x=alt.X("stringname", axis=alt.Axis(title="Nama Negara")),
        y=alt.Y('produksi:Q', axis=alt.Axis(title="Jumlah Produksi Kumulatif"))
    ).properties(title=f'Grafik {idx} Negara Terbesar berdasarkan Jumlah Produksi Minyak Mentah Kumulatif')
    st.altair_chart(chart, use_container_width=True)
    st.caption("Perbesar tampilan grafik dengan tombol kedua di grafik di atas")

def d1(year) :
    df1 = data
    df1 = df1.loc[df1['tahun'] == year]
    df1 = df1.sort_values(["produksi"], ascending=False)
    df1["nama"] = df1["kode_negara"].apply(searchCode)
    df1["region"] = df1["kode_negara"].apply(searchRegion)
    df1["sub-region"] = df1["kode_negara"].apply(searchSubRegion)
    column_names = ["nama", "kode_negara", "region","sub-region","produksi"]
    df1 = df1.reindex(columns=column_names)
    df1.rename(columns={'nama': 'Nama', 'kode_negara': 'Kode Negara', 'region': 'Region', 'sub-region': 'Sub-Region', 'produksi': 'Produksi'}, inplace=True, errors='raise')
    dfResult = df1.reset_index(inplace = False, drop = True)
    dfResult = dfResult[:1]
    st.table(dfResult)
    
def d12() :
    df = data
    df = df.drop('tahun', axis=1)
    df = df.groupby(['kode_negara'], as_index=False)['produksi'].sum()
    df = df.sort_values(["produksi"], ascending=False)
    df["nama"] = df["kode_negara"].apply(searchCode)
    df["region"] = df["kode_negara"].apply(searchRegion)
    df["sub-region"] = df["kode_negara"].apply(searchSubRegion)
    column_names = ["nama", "kode_negara", "region","sub-region","produksi"]
    df = df.reindex(columns=column_names)
    df.rename(columns={'nama': 'Nama', 'kode_negara': 'Kode Negara', 'region': 'Region', 'sub-region': 'Sub-Region', 'produksi': 'Produksi'}, inplace=True, errors='raise')
    dfResult = df.reset_index(inplace = False, drop = True)
    dfResult = dfResult[:1]
    st.table(dfResult)

def d2(year) :
    df1 = data
    df1 = df1.loc[df1['tahun'] == year]
    df1 = df1.sort_values(["produksi"], ascending=True)
    df1 = df1[df1["produksi"] != 0]
    df1["nama"] = df1["kode_negara"].apply(searchCode)
    df1["region"] = df1["kode_negara"].apply(searchRegion)
    df1["sub-region"] = df1["kode_negara"].apply(searchSubRegion)
    column_names = ["nama", "kode_negara", "region","sub-region","produksi"]
    df1 = df1.reindex(columns=column_names)
    df1.rename(columns={'nama': 'Nama', 'kode_negara': 'Kode Negara', 'region': 'Region', 'sub-region': 'Sub-Region', 'produksi': 'Produksi'}, inplace=True, errors='raise')
    dfResult = df1.reset_index(inplace = False, drop = True)
    dfResult = dfResult[:1]
    st.table(dfResult)
    
def d22() :
    df = data
    df = df.drop('tahun', axis=1)
    df = df.groupby(['kode_negara'], as_index=False)['produksi'].sum()
    df = df.sort_values(["produksi"], ascending=True)
    df = df[df["produksi"] != 0]
    df["nama"] = df["kode_negara"].apply(searchCode)
    df["region"] = df["kode_negara"].apply(searchRegion)
    df["sub-region"] = df["kode_negara"].apply(searchSubRegion)
    column_names = ["nama", "kode_negara", "region","sub-region","produksi"]
    df = df.reindex(columns=column_names)
    df.rename(columns={'nama': 'Nama', 'kode_negara': 'Kode Negara', 'region': 'Region', 'sub-region': 'Sub-Region', 'produksi': 'Produksi'}, inplace=True, errors='raise')
    dfResult = df.reset_index(inplace = False, drop = True)
    dfResult = dfResult[:1]
    st.table(dfResult)
    

def d3(year) :
    df1 = data
    df1 = df1.loc[df1['tahun'] == year]
    df1 = df1.sort_values(["produksi"], ascending=True)
    df1 = df1[df1["produksi"] == 0]
    df1["nama"] = df1["kode_negara"].apply(searchCode)
    df1["region"] = df1["kode_negara"].apply(searchRegion)
    df1["sub-region"] = df1["kode_negara"].apply(searchSubRegion)
    column_names = ["nama", "kode_negara", "region","sub-region","produksi"]
    df1 = df1.reindex(columns=column_names)
    df1.rename(columns={'nama': 'Nama', 'kode_negara': 'Kode Negara', 'region': 'Region', 'sub-region': 'Sub-Region', 'produksi': 'Produksi'}, inplace=True, errors='raise')
    dfResult = df1.reset_index(inplace = False, drop = True)
    st.table(dfResult)

def d32() :    
    df = data
    df = df.drop('tahun', axis=1)
    df = df.groupby(['kode_negara'], as_index=False)['produksi'].sum()
    df = df.sort_values(["produksi"], ascending=True)
    df = df[df["produksi"] == 0]
    df["nama"] = df["kode_negara"].apply(searchCode)
    df["region"] = df["kode_negara"].apply(searchRegion)
    df["sub-region"] = df["kode_negara"].apply(searchSubRegion)
    column_names = ["nama", "kode_negara", "region","sub-region","produksi"]
    df = df.reindex(columns=column_names)
    df.rename(columns={'nama': 'Nama', 'kode_negara': 'Kode Negara', 'region': 'Region', 'sub-region': 'Sub-Region', 'produksi': 'Produksi'}, inplace=True, errors='raise')
    dfResult = df.reset_index(inplace = False, drop = True)
    st.table(dfResult)

# Layout Page
st.header("Fitur 1")
st.subheader("Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N")
st.write("Tulis sebuah nama lengkap negara untuk menampilkan grafik")
nama = st.text_input('Nama Negara', 'Australia', placeholder='Australia')
if nama :
    a(nama)

st.markdown("***")
st.header("Fitur 2")
st.subheader("Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T")
st.write("Tulis sebuah tahun untuk menampilkan grafik")
year =  st.slider("Tahun", step=1, max_value=2015,min_value=1971, key=1)
st.write("Tulis sebuah angka N untuk menampilkan grafik N negara (max : 110)")
idx = st.number_input('Angka', step=1, key=1, value=1)
b(year,idx)

st.markdown("***")
st.header("Fitur 3")
st.subheader("Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif keseluruhan tahun")
st.write("Tulis sebuah angka N untuk menampilkan grafik N negara (max : 137)")
idx1 = st.number_input('Angka',step=1, key=2, value=1)
c(idx1)

st.markdown("***")
st.header("Information")
st.subheader("Negara dengan Jumlah Produksi Terbesar Tahun T")
year =  st.slider("Tahun", step=1, max_value=2015,min_value=1971, key=2)
d1(year)
st.subheader("Negara dengan Jumlah Produksi Terbesar Keseluruhan Tahun")
d12()

st.markdown("***")
st.subheader("Negara dengan Jumlah Produksi Terkecil Tahun T")
year =  st.slider("Tahun", step=1, max_value=2015,min_value=1971, key=3)
d2(year)
st.subheader("Negara dengan Jumlah Produksi Terkecil Keseluruhan Tahun")
d22()

st.markdown("***")
st.subheader("Negara dengan Jumlah Produksi 0 Tahun T")
year =  st.slider("Tahun", step=1, max_value=2015,min_value=1971, key=4)
d3(year)
st.subheader("Negara dengan Jumlah Produksi 0 Keseluruhan Tahun")
d32()

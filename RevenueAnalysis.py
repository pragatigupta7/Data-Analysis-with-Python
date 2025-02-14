import pandas as pd
import plotly.graph_objects as go
import streamlit as st

@st.cache_data

def load_data():
    df=pd.read_csv(r"Spotify Quarterly.csv")
    df=df.drop(columns=['MAUs',
       'Premium MAUs', 'Ad MAUs', 'Premium ARPU'])

    df=df.dropna()
    df.index=range(1,len(df)+1)
    df['Date']=pd.to_datetime(df['Date'],dayfirst=True)
    return df
st.set_page_config(
    layout='wide',
    page_title='Spotify Revenue Analysis',
    page_icon="📊"
)

with st.spinner(" Loading Data..."):
    
    
   # time.sleep(5)
    df=load_data()
    st.sidebar.success("Spotify :green[Revenue Analysis]")
st.title("Spotify :green[Revenue Analysis]")
st.markdown("Revenue Data(* all values in € million )")
st.dataframe(df)
fig=go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Total Revenue'], mode='lines', name='Total Revenue'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Cost of Revenue'], mode='lines', name='Cost of Revenue'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Gross Profit'], mode='lines', name='Gross Profit'))
fig.update_layout(template='plotly_dark',yaxis_title='Revenues(€ million)')
st.subheader("Revenue :violet[Generated] (Quarterly)",divider=True)
c1,c2=st.columns([5,2])

c1.plotly_chart(fig,use_container_width=True)
c2.dataframe(df[['Date','Total Revenue','Cost of Revenue','Gross Profit']])
c2.markdown("""<h6 style="text-align: right;">*values(€ million)</h6> """,unsafe_allow_html=True)


fig=go.Figure()
fig.add_trace(go.Bar(x=df['Date'], y=df['Premium Gross Profit'], name='Premium Gross Profit'))
fig.add_trace(go.Bar(x=df['Date'], y=df['Premium Cost Revenue'], name='Premium Cost Revenue'))
fig.add_trace(go.Bar(x=df['Date'], y=df['Premium Revenue'], name='Premium Revenue'))

fig.update_layout(yaxis_title='Spotify\'s Premium Revenues(€ million)',
                  barmode='group',template='plotly_dark')
st.subheader(":green[Premium] Revenues",divider='green')

c1,c2=st.columns([5,2])

c1.plotly_chart(fig,use_container_width=True)
c2.dataframe(df[['Date','Premium Gross Profit','Premium Cost Revenue','Premium Revenue']])
c2.markdown("""<h6 style="text-align: right;">*values(€ million)</h6> """,unsafe_allow_html=True)

fig=go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Ad Revenue'], mode='lines', name='Ad Revenue'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Ad Cost of revenue'], mode='lines', name='Ad Cost of revenue'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Ad gross Profit'], mode='lines', name='Ad gross Profit'))
fig.update_layout(template='plotly_dark',yaxis_title='Revenues(€ million)')
st.subheader(":violet[Ad] Revenues",divider='violet')
c1,c2=st.columns([5,2])

c1.plotly_chart(fig,use_container_width=True)
c2.dataframe(df.iloc[:,[0,7,8,9]])
c2.markdown("""<h6 style="text-align: right;">*values(€ million)</h6> """,unsafe_allow_html=True)


fig=go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Sales and Marketing Cost'], mode='none', name='Sales and Marketing Cost',fill='tozeroy'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Research and Development Cost'], mode='none', name='Research and Development Cost',fill='tozeroy'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Genreal and Adminstraive Cost'], mode='none', name='Genreal and Adminstraive Cost',fill='tozeroy'))
fig.update_layout(template='plotly_dark',yaxis_title='Miscellanous Costs(€ million)')
st.subheader('Miscellaneous :green[Costs]',divider='green')
c1,c2=st.columns([5,2])

c1.plotly_chart(fig,use_container_width=True)
c2.dataframe(df.iloc[:,[0,9,10,11]])
c2.markdown("""<h6 style="text-align: right;">*values(€ million)</h6> """,unsafe_allow_html=True)

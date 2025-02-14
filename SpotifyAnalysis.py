#python -m streamlit run Spotify\SpotifyAnalysis.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
@st.cache_data
def load_data():
    df=pd.read_csv(r"tracks.csv.zip")
    df=df.sort_values('popularity',ascending=False)
    df['artists']=df['artists'].apply(lambda x:x[1:-1].replace('\'',""))
    df['duration_ms']=df['duration_ms'].apply(lambda x:str(x//60000)+":"+str((x//10000)%60))
    df['id_artists']=df['id_artists'].apply(lambda x:x[1:-1].replace('\'',''))
    df['explicit']=df['explicit'].apply(lambda x:'Yes' if x==1 else 'No')
    df=df.drop(columns='id')
    df=df.rename(columns={'duration_ms':'duration',
                       'id_artists':'artists_id'})
    df=df.drop_duplicates().dropna()
    df.index=range(1,len(df)+1)
    return df



st.set_page_config(
    layout='wide',
    page_title='Spotify Data Analysis',
    page_icon="📊"
)
#loading the data
with st.spinner(" Loading Data..."):
    
    
   # time.sleep(5)
    df=load_data()
    st.sidebar.success("Spotify :green[Analysis]")
st.title("Spotify :green[Analysis]")
numeric_df=df.select_dtypes(include='number')
corr_matrix = numeric_df.corr()

# Create a heatmap of the correlation matrix
fig = px.imshow(
    corr_matrix,
    text_auto=True,
    height=800,
    width=800,
    color_continuous_scale=px.colors.sequential.speed,
    aspect='auto',

)

# Center the title
st.dataframe(df)
st.subheader("Pairwise Correlation of :violet[Music Attributes]")

# Show the figure
st.plotly_chart(fig,use_container_width=True)

fig=make_subplots(rows=3,cols=3,subplot_titles=('<i>liveness', '<i>danceability', '<i>energy', '<i>loudness', '<i>speechiness', '<i>acousticness', '<i>liveness', '<i>valence', '<i>tempo'))
fig.add_trace(go.Histogram(x=df['liveness'],name='liveness'),row=1,col=1)
fig.add_trace(go.Histogram(x=df['danceability'],name='danceability'),row=1,col=2)

fig.add_trace(go.Histogram(x=df['energy'],name='energy'),row=1,col=3)
fig.add_trace(go.Histogram(x=df['loudness'],name='loudness'),row=2,col=1)
fig.add_trace(go.Histogram(x=df['speechiness'],name='speechiness'),row=2,col=2)
fig.add_trace(go.Histogram(x=df['acousticness'],name='acousticness'),row=2,col=3)
st.header("",divider='violet')
fig.add_trace(go.Histogram(x=df['liveness'],name='liveness'),row=3,col=1)
fig.add_trace(go.Histogram(x=df['valence'],name='valence'),row=3,col=2)
fig.add_trace(go.Histogram(x=df['tempo'],name='tempo'),row=3,col=3)

fig.update_layout(height=1900,width=1900,title_text='<b>Feature Distribution')
fig.update_layout(template='plotly_dark',title_x=0.5)
st.markdown("""
###  <span style="color:green">Spotify Music</span> <span style="color:purple">Feature Distribution</span>
""", unsafe_allow_html=True)
st.plotly_chart(fig,use_container_width=True)
df['release_date']=df['release_date'].apply(lambda x : x[:4])
fig=px.area(df.groupby('release_date',as_index=False).count().sort_values(by='name',ascending=False).sort_values(by='release_date'),x='release_date',y='name',markers=True,labels={'name':'Total songs','release_date':'Release_Year'},color_discrete_sequence=['green'],template='plotly_dark',title=" ")
fig.update_xaxes(dtick=5)

fig.update_layout(hovermode='x',title_x=0.5)

st.subheader("",divider='violet')
st.subheader("Year by Year Songs Collection")
c1,c3,c2=st.columns([5,1,2])
c1.plotly_chart(fig,use_container_width=True)

d1=pd.DataFrame()
totalsong=[]
l=list(df['release_date'].unique())
for i in l:
    totalsong.append((list(df['release_date'])).count(i))
d1['Total songs']=totalsong
c3.metric("Tracks Added in last 5 years",value="",delta="57.7k")
d1['Year']=l
d1=d1.sort_values(by='Year',ascending=False)
d1.index=range(1,len(d1)+1)

c2.dataframe(d1,use_container_width=True)

# Song recorded by each of top 50 artists
st.subheader(' List of Tracks Recorded by Each Artist(Top 50)')
c1,c2=st.columns([5,2])
fig=px.bar(df.groupby('artists',as_index=False).count().sort_values(by='name',ascending=False).head(50),x='artists',y='name',labels={'name':'Total Tracks'},width=1000,color_discrete_sequence=['green'],text='name')
c1.plotly_chart(fig,use_container_width=True)
grouped_df = df.groupby('artists', as_index=False)['name'].count().sort_values(by='name', ascending=False).head(50)
grouped_df=grouped_df.rename(columns={'name':'Total Tracks'})
grouped_df.index=range(1,len(grouped_df)+1)
c2.dataframe(grouped_df,use_container_width=True)

fig=px.bar(df.groupby('artists',as_index=False).sum().sort_values(by='popularity',ascending=False).head(30),x='artists',y='popularity',color_discrete_sequence=['lightgreen'],template='plotly_dark',text='popularity',title='<b>Top 30 Popular Singers')
st.plotly_chart(fig,use_container_width=True)
st.subheader("",divider='violet')

c1,c2=st.columns(2)
fig=px.area(df[df['explicit']=='Yes'].groupby('release_date',as_index=False).count().sort_values(by='name',ascending=False).
            sort_values(by='release_date'),x='release_date',y='name',labels={'name':'Total Tracks',
                'release_date':'Release_Year'},markers=True,color_discrete_sequence=['red'],template='plotly_dark',
                    )

fig.update_layout(hovermode='x')
fig.update_xaxes(dtick=10)
fig.update_yaxes(dtick=700)
c1.subheader('Total Explicit Tracks v/s Year Released')
c1.plotly_chart(fig,use_container_width=True)
c2.markdown("""
###  Popularity Based On <span style="color:red">Explicit</span> Content
""", unsafe_allow_html=True)
c2.plotly_chart(px.box(df[::5],x='explicit',y='popularity',color='explicit',template='plotly_dark',color_discrete_sequence=['magenta','cyan']),use_container_width=True)

p=pd.DataFrame()

p=df.iloc[:,[3,6]].sort_values(by='release_date',ascending=False)
p.index=range(1,len(p)+1)

filtered_p = p[:200000]

# Create a column for count of explicit content per release_date
filtered_p['explicit_count'] = filtered_p['explicit'] == 'Yes'

# Group by release_date and sum explicit counts
grouped_p = filtered_p.groupby('release_date', as_index=False)['explicit_count'].sum()

# Create the pie chart f
fig = px.pie(
    grouped_p,
    values='explicit_count',
    names='release_date',
    
    template='plotly_dark'
)
c1,c2=st.columns(2)
c1.subheader('Inc. in Explicit content over Time')
c1.plotly_chart(fig,use_container_width=True)
c2.subheader(":rainbow[Tempo] v/s Popularity")
c2.plotly_chart(px.histogram(df[::5], 'tempo', 'popularity',template='plotly_dark', color_discrete_sequence=['sienna'],marginal='box'))
c2.metric("\t\t\tPreferred Tempo -> 118-122 BPM","")

c1,c2=st.columns(2)
fig=px.scatter(df[::10],x='speechiness',y='popularity',color='speechiness',color_continuous_scale=px.colors.sequential.Plasma,template='plotly_dark')
fig.update_xaxes(dtick=0.1)
c1.header(":violet[Speechiness] v/s Popularity")


c1.plotly_chart(fig,use_container_width=True)

c2.header("Loudness & :orange[Energy] Correlation ")
c2.plotly_chart(px.histogram(df[::5],'loudness','energy',template='plotly_dark',color_discrete_sequence=['orange']),use_container_width=True)






import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("Hello World")
st.header("this is streamlit")
st.subheader("you will be able to start creating things")

st.text("this is how you will create your project")
st.code("a = 123\n\
        import pandas \n"\
            "plt.show()")

st.markdown("---")
st.header("lets display some data")

df = pd.read_csv("https://raw.githubusercontent.com/ArtMarciano/datasets/refs/heads/main/tips.csv")
st.dataframe(df)

tip_range = st.slider("Filter by tip amount", min_value =0.0, max_value = 15.0, value=5.0)

filtered_df = df[df['tip'] <= tip_range]
st.write(f'Showing {len(filtered_df)} rows')
st.dataframe(filtered_df)

fig, ax = plt.subplots()
ax.hist(filtered_df['tip'],bins = 15, color = 'steelblue', alpha =.7)
ax.set_xlabel('Tip amount ($)')
ax.set_ylabel('Count')
ax.set_title('Distribution of tips')
st.pyplot(fig)

st.markdown('---')
st.subheader('Summary')

col1, col2, col3 = st.column(3)
col1.metric(label = 'total rows', value = len(filtered_df))
col2.metric(label = 'Avg Tip', value = f'${filtered_df['tip'].mean():.2f}')
col3.metric(label = 'Avg Bill', value = f'{filtered_df['total_bill'].mean():.2f})
            
chart_col1 = 

with chart_co1:
    st.write('tip distribution)
    fig1, ax1 = plt.subplot()
    ax1.hist(filtered_df['tip'], bins = 15, color = 'blue', alpha = .5
    ax1.set_xlabel('Tip ($)')
    sy.pyplot(fig1)

day = sidebarselectbox('Day of the week', ('All','Thur', 'Friday', 'Sat', 'Sun'))
if day != 'All':
    filtered_df = [filtered_df[filtered_df['day'] == day]
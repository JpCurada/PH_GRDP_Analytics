import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(
   page_title="PH GRDP Analytics",
   page_icon=":bar_chart",
   initial_sidebar_state="expanded",
   layout="wide"
   
)

st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,)

df_ph_grdp = pd.read_excel('PH_GRDP_data.xlsx', sheet_name='GRDP PH Total')
df_growthrate = pd.read_excel('PH_GRDP_data.xlsx', sheet_name='GRDP Growth Rate')

def df_data(constant_current):
    df = pd.read_excel('PH_GRDP_data.xlsx', sheet_name=constant_current)
    return df

years = np.array([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])

def grdp_by_region(df, years_array, chosen_regions):

    df_plot = pd.DataFrame(years_array, columns=['Year'])

    for index, row in df.iterrows():
        for region in list(chosen_regions):
            if row.REGION == region:
                list_of_values = list(row.values)
                list_of_values.pop(0)
                df_plot[region] = list_of_values
                
    return df_plot

def compare_regions_gdp_chart(df_regions_choice, chosen_regions, title):
    fig = go.Figure()
    for region in chosen_regions:
        fig.add_trace(go.Scatter(x= df_regions_choice['Year'].values, y=df_regions_choice[region].values, name=region, mode='lines+markers',
                                line=dict(width=3)))
    fig = fig.update_layout(title=title,xaxis_title='Year',yaxis_title='GDP Amount in Peso (₱)')
    return fig
    
def grdp_by_industry(years_array, selected_regions, selected_industry):
    
    df_plot = pd.DataFrame(years_array, columns=['Year'])
    
    for region in list(selected_regions):
        df = pd.read_excel('PH_industries_GRDP_data.xlsx', sheet_name=region)
        df_plot[region] = df[selected_industry].values
    
    return df_plot

def gdp_bar_chart(df, current_constant):
    fig = px.bar(df, y=current_constant, x='Year', text_auto=False,
                title=f"Total Philippine GRDP")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

def gdp_line_chart(df, constant_current):
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x= df['Year'].values, y=df[constant_current].values, name='Year', mode='lines+markers',
                                line=dict(width=3)))
    fig = fig.update_layout(title=f"Philippine GRDP Growth Rate",xaxis_title='Year',yaxis_title='Growth Rate')
    return fig

def release_data(constant_current, selected_regions):
    data = pd.read_excel('PH_GRDP_data.xlsx',sheet_name=f'GRate {constant_current}')
    data_df = pd.DataFrame(np.array([2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]), columns=['Year'])
    for region in list(selected_regions):
        data_df[region] = data[region].values 
    return data_df

def get_max_details(data):

    data_df = data.drop(columns='Year')
    max_grate = max([max(data_df[column].values) for column in data_df.columns])

    for column in data_df.columns:
        for idx, val in enumerate(data[column].values):
            if val == max_grate:
                year = data['Year'].values[idx]
                region = column    
    return max_grate, year, region

def get_min_details(data):

    data_df = data.drop(columns='Year')
    min_grate = min([min(data_df[column].values) for column in data_df.columns])

    for column in data_df.columns:
        for idx, val in enumerate(data[column].values):
            if val == min_grate:
                year = data['Year'].values[idx]
                region = column    
    return min_grate, year, region

def if_constant_or_current(cur_con):
    if cur_con == 'At Current Prices':
         return 'At Current Prices'
    else:
         return 'At 2018 Constant Prices'

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

with st.container():

    t1, t2 = st.columns(2)

    image = Image.open('ph_grdp_img.png')
    t1.image(image)

    t2.header('Philippine GRDP Analytics')
    t2.write("""The Philippine Gross Domestic Product (GDP) is a measure of the total economic output of the Philippines, 
    including the value of all goods and services produced in the country. It is the most widely used indicator of the economic 
    performance of a country and is often used to compare the economic growth of different countries. The GDP of a region, 
    such as the Gross Domestic Product of the Philippines, is often referred to as the Gross Domestic Product at Regional 
    Prices (GDPRP). The GDPRP is calculated by measuring the value of all goods and services produced in a region, regardless 
    of where they are consumed. It is a measure of the economic output of a region and is used to compare the economic performance of 
    different regions within a country.""")

    t2.write("""This dashboard aims to help data analysts and economists in analyzing Gross Domestic Regional Product (GRDP) 
    of regions within the Philippines from 2000 to 2021. This application provides insights to users by giving visualization charts 
    and downloadable CSV files of selected parameters by the user.""")

    t2.caption("""***Note: Change your theme to 'Dark' theme in settings for better visualization.***""")
      
    st.markdown('---')
   
    st.subheader("Terms of Definitions")

    st.write('***GRDP:***') 
    st.caption('Gross Regional Domestic Product (GRDP) is a metric used to assess the economic output of a specific region. It takes into account the value of all goods and services produced within the region, and is often reported in terms of growth rate or change over time. GRDP is typically reported in real terms, meaning that it is adjusted for inflation and reflects the actual purchasing power of the economy. This allows for comparison of economic performance between different time periods or regions.')
    st.write('***At Current Prices:***' )
    st.caption('Current prices, also known as nominal prices, refer to the actual price of a good or service at a specific point in time.')
    st.write('***At 2018 Constant Prices:***')
    st.caption('Constant prices, on the other hand, are adjusted for inflation and represent the real value of a good or service. Constant prices are used to compare economic performance or indicators over time and across regions, as they reflect the purchasing power of an economy rather than just the nominal prices of goods and services. Constant prices are often referred to as "real" prices because they reflect the actual value of goods and services rather than just the nominal price. The Philippine Statistics Authority (PSA) set the year 2018 as the reference datum for constant prices.')

   
    st.markdown('---')

    st.subheader('Gross Domestic Regional Product')
    cur_con = st.radio('Gross Domestic Product of selected regions and selected industry from year 2000 to 2021',('At Current Prices', 'At 2018 Constant Prices')         
    constant_or_current = if_constant_or_current(cur_con)
   
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    regions_col, industry_col = st.columns(2)
    with regions_col:   
        selected_region = st.selectbox('Select a region you want to contrast:', ('Luzon', 'Visayas', 'Mindanao', 'All Regions'))
        def get_selected_regions(selected_region):
            if selected_region == 'All Regions':
                selected_regions = ('NCR', 'CAR', 'Region I','Region II', 'Region III', 'Region IVA', 'Region IVB', 'Region V',
                    'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI', 'Region XII', 'Region XIII','BARMM')
            elif selected_region == 'Luzon':
                selected_regions = ('NCR', 'CAR', 'Region I','Region II', 'Region III', 'Region IVA', 'Region IVB', 'Region V')
            elif selected_region == 'Visayas':
                selected_regions = ('Region VI', 'Region VII', 'Region VIII')
            else:
                selected_regions = ('Region IX', 'Region X', 'Region XI', 'Region XII', 'Region XIII','BARMM')
            return selected_regions

        selected_regions = get_selected_regions(selected_region)
        at_grdp_prices_data = grdp_by_region(df_data(constant_or_current), years, selected_regions)
        
    
    with industry_col:
        selected_industry = st.selectbox('Choose an Industry:', ( 'Agriculture, Forestry and Fishing', 'Production', 'Mining and Quarrying',
            'Manufacturing', 'Electricity, Steam, Water and Waste Management', 'Construction', 'Services', 'Wholesale and Retail Trade: Repair of Motor Vehicles and Motorcycles',
            'Transportation and Storage', 'Accomodation and Food Service Activities', 'Information and Communication', 'Financial and Insurance Activities',
            'Real Estate and Ownership of Dwellings', 'Professional and Business Services', 'Public Administration and Defense: Compulsory Social Activities',
            'Education', 'Human Health and Social Work Activities', 'Other Services'))
        gdp_industry_data = grdp_by_industry(years, selected_regions, selected_industry)
    
    st.markdown('---')

    c1,c2,c3 = st.columns(3)
    c1.metric(f'Lowest GRDP of 2021', f"₱{int(np.min(at_grdp_prices_data.drop(columns='Year').iloc[-1:].values)):,}",f"{[col for col in at_grdp_prices_data.columns for val in at_grdp_prices_data[col].values if val == np.min(at_grdp_prices_data.drop(columns='Year').iloc[-1:].values)][0]}", delta_color="off")
    c2.metric(f'Top Contributor for the Selected Industry', f"{get_max_details(gdp_industry_data)[2]}", f"Average of ₱{int(np.mean(gdp_industry_data[get_max_details(gdp_industry_data)[2]].values)):,}", delta_color="off")
    c3.metric(f'Highest GRDP of 2021', f"₱{int(np.max(at_grdp_prices_data.iloc[-1:].values)):,}", f"{[col for col in at_grdp_prices_data.columns for val in at_grdp_prices_data[col].values if val == np.max(at_grdp_prices_data.iloc[-1:].values)][0]}", delta_color="off")

    region_chart_col, industry_chart_col = st.columns(2)
    region_chart_col.plotly_chart(compare_regions_gdp_chart(at_grdp_prices_data, selected_regions, f'{constant_or_current}'), use_container_width=True)
    industry_chart_col.plotly_chart(compare_regions_gdp_chart(gdp_industry_data, selected_regions, f"GRDP of {selected_industry} Industry"), use_container_width=True)


    st.markdown('---')

with st.container():
    data = release_data(constant_or_current, selected_regions)
    a,b,c = st.columns(3)
    a.metric("All-Time Low Performing Region", f"{get_min_details(data)[2]}", f"{get_min_details(data)[0]} % for {get_min_details(data)[1]}")
    b.metric(f"GRDP 2021 Growth Rate of {selected_region}", f"{round(np.mean(data.drop(columns='Year').iloc[-1:].values[0]),2)} %", f"{round(np.mean(data.drop(columns='Year').iloc[-1:].values[0]) - np.mean(data.drop(columns='Year').iloc[-2:-1].values[0]),2)}%")
    c.metric("All-Time High Performing Region", f"{get_max_details(data)[2]}", f"{get_max_details(data)[0]} % for {get_max_details(data)[1]}")

    st.plotly_chart(compare_regions_gdp_chart(data, selected_regions, f'GRDP Growth Rate'), use_container_width=True)

    st.markdown('---')

    c1_, c2_, c3_ = st.columns(3)
    c1_.metric('All-Time Growth Percentage', f"↑ {round((df_ph_grdp[constant_or_current].values[-1]/df_ph_grdp[constant_or_current].values[0])*100,2)} %", "from 2000 to 2021", delta_color="off")
    c2_.metric('All-Time Low', f"{get_min_details(df_growthrate)[1]-1} to {get_min_details(df_growthrate)[1]}", f"{np.min(df_growthrate[constant_or_current].values)} % ")
    c3_.metric('All-Time GRDP Added Value', f"+ ₱{round(df_ph_grdp[constant_or_current].values[-1] - df_ph_grdp[constant_or_current].values[0],2):,}", "from 2000 to 2021", delta_color="off")
    gdrp_amount_col, grdp_growthrate_col = st.columns(2)
    gdrp_amount_col.plotly_chart(gdp_bar_chart(df_ph_grdp, constant_or_current), use_container_width=True)
    grdp_growthrate_col.plotly_chart(gdp_line_chart(df_growthrate, constant_or_current), use_container_width=True)

    with st.expander("Downloadable Data"):

        d1,d2 = st.columns(2)
        d1.subheader(f'GRDP of regions within {selected_region}')
        d1.dataframe(at_grdp_prices_data)
        at_grdp_prices_data_csv = convert_df(at_grdp_prices_data)
        d1.download_button(
            label="Download data as CSV",
            data=at_grdp_prices_data_csv,
            file_name='at_grdp_prices_data.csv',
            mime='text/csv',
        )

        d2.subheader(f'{selected_industry}')
        d2.dataframe(gdp_industry_data)
        gdp_industry_data_csv = convert_df(gdp_industry_data)
        d2.download_button(
            label="Download data as CSV",
            data=at_grdp_prices_data_csv,
            file_name='gdp_industry_data.csv',
            mime='text/csv',
        )

        do1,do2,do3 = st.columns(3)

        do1.subheader(f'GRDP Growth Rate of {selected_region}')
        do1.dataframe(data)
        data_csv = convert_df(data)
        do1.download_button(
            label="Download data as CSV",
            data=data_csv,
            file_name='data.csv',
            mime='text/csv',
        )

        do2.subheader(f'Total Philippine GRDP')
        do2.dataframe(df_ph_grdp)
        df_ph_grdp_csv = convert_df(df_ph_grdp)
        do2.download_button(
            label="Download data as CSV",
            data=df_ph_grdp_csv,
            file_name='df_ph_grdp.csv',
            mime='text/csv',
        )

        do3.subheader(f'Philippine GRDP Growth Rate')
        do3.dataframe(df_growthrate)
        df_growthrate_csv = convert_df(df_growthrate)
        do3.download_button(
            label="Download data as CSV",
            data=df_growthrate_csv,
            file_name='df_growthrate.csv',
            mime='text/csv',
        )
    
    st.markdown('---')
    st.write("The creator of this page gives credits or acknowledgement to Philippine Statistics Authority (PSA) as the data used in this project are from their database.")
    st.caption("Terms of use of PSA clearly stated that:")
    st.caption('"The statistical tables (or datasets) including documents (collectively as material) on this site are classified under Open Data with Creative Commons Attribution License (cc-by). This means that you are free to share (copy and redistribute) the material in any medium or format; remix, transform and build upon the material without any restrictions other than proper source attribution."')
    st.caption("""***Source: https://openstat.psa.gov.ph/Database/Gross-Regional-Domestic-Product***""")
    st.write("""***— John Paul M. Curada***
    [@LinkedIn](https://www.linkedin.com/in/jp-curada-20b69b214/) [@Twitter](https://twitter.com/jpcodesss)""")


    

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from flask import Flask, request, jsonify
import warnings
warnings.filterwarnings('ignore')

import mysql.connector

db_config = {
    'host':"database-1.cmc9nvfmf9i4.eu-north-1.rds.amazonaws.com",
    'user':"admin",
    'password':"admin123",
    'database':"Emission_data"
}


app = Flask(__name__)
@app.route('/emission', methods=['POST'])
def emission_calculation():
    data = request.json
    username = data['username']
    date = data['date']
    ctype = data['ctype']
    units = data['units']
    #co2_factor = pd.read_csv(r'co2factor.csv')
    
    conn = mysql.connector.connect(**db_config)
    query = "SELECT * FROM emission_data"
    final_emission_df = pd.read_sql_query(query, conn)
    query = "SELECT * FROM co2factor"
    co2_factor = pd.read_sql_query(query, conn)
    conn.close()
  
    #final_emission_df = pd.read_csv(r'emission_data.csv')
    
    final_emission_df = loading_data(username,date,ctype,units,co2_factor,final_emission_df)
    

    #final_emission_df.to_csv(r'emission_data.csv',index = False)
    print(username)
    print(final_emission_df)
    
    emission_ld,emission_lm = emission_display(final_emission_df,username)
    return jsonify({"emission_ld": emission_ld, "emission_lm": emission_lm})


# In[14]:


def emission_display(final_emission_df,user):
    #Month Emission
    df_sub = final_emission_df[final_emission_df['User'] == user]
    df_sub['Date'] = pd.to_datetime(df_sub['Date'])
    df_sub['Latest_Month'] = df_sub['Date'].dt.to_period('M')
    max_period =max(df_sub['Latest_Month'])
    df_sub=df_sub[df_sub['Latest_Month'] == max_period]
    latest_month_emission = df_sub.groupby(['User', 'Latest_Month'])['Total_Emission'].sum().reset_index()
    total_emission_latest_month = latest_month_emission['Total_Emission'].sum()
    print(total_emission_latest_month)
    #Date Emissiond
    max_date =max(df_sub['Date'])
    df_sub = df_sub[df_sub['Date'] == max_date]
    latest_emission = df_sub.groupby(['Date'])['Total_Emission'].sum().reset_index()
    latest_emission= df_sub['Total_Emission'].sum()
    print(latest_emission)
    return latest_emission,total_emission_latest_month
    


# In[4]:


#Loading new data

def loading_data(username,date,ctype,units,co2_factor,final_emission_df):
    factor = co2_factor.loc[co2_factor['Category'] == ctype, 'Value'].item()
    print("Factor : ",factor)
    print(type(factor))
    print("Units : ",units)
    print(type(units))
    units = int(units)
    new_row = {'User':username, 'Date':date,'Consumption_type': ctype,'Units':units,'Total_Emission': factor * units}
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    insert_query = "INSERT INTO emission_data (User, Date, Consumption, Units, Total_Emission) VALUES (%s, %s, %s, %s, %s)"
    user_data = (username, date, ctype, units, factor * units)
    cursor.execute(insert_query, user_data)
    conn.commit()
    conn.close()
    final_emission_df = pd.concat([final_emission_df, pd.DataFrame([new_row])], ignore_index=True)
    return final_emission_df




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


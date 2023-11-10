import pandas as pd
from flask import Flask, request, jsonify
import requests
import warnings
warnings.filterwarnings('ignore')

url2 = "http://emailscript:5000/email"


import mysql.connector

db_config = {
    'host':"database-1.cmc9nvfmf9i4.eu-north-1.rds.amazonaws.com",
    'user':"admin",
    'password':"admin123",
    'database':"userdb"
}



app = Flask(__name__)
@app.route('/user', methods=['POST'])
def check_user():
    data = request.json
    username = data['username']
    conn = mysql.connector.connect(**db_config)
    query = "SELECT * FROM users"
    final_user_df = pd.read_sql_query(query, conn)
    conn.close()
    #final_user_df = pd.read_csv(r'user.csv')
    if username in final_user_df['name'].values:
        user_subset = final_user_df[final_user_df['name'] == username]
        user_json = user_subset.to_dict(orient='records')
        return jsonify({"userfound": "yes", "userdata": user_json})
    else:
        return jsonify({"userfound": "no"})   


@app.route('/newuser', methods=['POST'])
def new_user():
    data = request.json
    username = data['username']
    email = data['email']
    age = data['age']
    food_style = data['food_style']
    country = data['country']
    #final_user_df = pd.read_sql_query(query, conn)
    #final_user_df = pd.read_csv(r'user.csv')
    #new_row = {'name':username, 'email':email, 'age':age, 'country':country,'food_preference':food_style}
    #final_user_df = pd.concat([final_user_df, pd.DataFrame([new_row])], ignore_index=True)
    #final_user_df.to_csv(r'user.csv',index = False)
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (name, email, age, country, food_preference) VALUES (%s, %s, %s, %s, %s)"
    user_data = (username, email, age, country, food_style)
    cursor.execute(insert_query, user_data)
    conn.commit()
    conn.close()
    
    response = requests.post(url2, json={"username": username,"email": email})
    if response.status_code == 200:
        return jsonify({"usercreation": "successfully created and mail sent"})
    else:
        return jsonify({"usercreation": "successfully created and mail not sent"})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



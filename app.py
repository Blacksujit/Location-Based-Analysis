from flask import Flask, render_template, request , send_file , render_template_string
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)

# Load and clean the dataset
df = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\Machine Learning Projects\\Location_based_analysis\\data\\Dataset .csv')
df.dropna(subset=['Latitude', 'Longitude', 'City', 'Average Cost for two', 'Aggregate rating', 'Cuisines', 'Restaurant Name'], inplace=True)

def create_map(city):
    filtered_data = df[df['City'] == city]
    if filtered_data.empty:
        return None

    m = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    
    for idx, row in filtered_data.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']],
                      popup=f"{row['Restaurant Name']} - {row['Cuisines']} - {row['Aggregate rating']}",
                      icon=folium.Icon(color='blue', icon='info-sign')).add_to(marker_cluster)
    
    return m

# @app.route('/get-html')
# def get_html():
#     html_file_path = 'C:\\Users\\HP\\OneDrive\\Desktop\\Machine Learning Projects\\Location_based_analysis\\index.html'  # Replace with your actual HTML file path
#     return send_file(html_file_path)

@app.route('/')
def home():
    # html_response = requests.get(' http://127.0.0.1:5000/get-html')
    # html_content = html_response.text
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
    city = request.form['city']
    map_obj = create_map(city)
    if map_obj is None:
        return render_template('error.html', message=f"No data available for {city}")

    map_path = f'static/{city}_map.html'
    map_obj.save(map_path)
    return render_template('result.html', city=city, map_path=map_path)

if __name__ == '__main__':
    app.run(debug=True)

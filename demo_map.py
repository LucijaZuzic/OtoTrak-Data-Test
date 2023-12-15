import mplleaflet
from utilities import *
import folium
import io
from PIL import Image
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def save_trajmap(longitudes, latitudes, subdir_name, filename):
    figss, ax = plt.subplots() 
    ax.plot(longitudes, latitudes)  
    #mplleaflet.display(fig=figss) 
    # Save the OpenStreetMap plot as a PNG image
    #plt.savefig("map_gps/" + subdir_name + "/" + filename + ".png", bbox_inches='tight', pad_inches=0.2, dpi=300)  # Adjust parameters as needed
    #plt.close(figss)  
    #print("Image saved as 'map_image.png'")
    m = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=24)  # You can adjust the zoom level (zoom_start)
     
    combined_array = np.column_stack((latitudes, longitudes))
    # Add a marker for the specified location
    folium.PolyLine(combined_array).add_to(m)  # You can customize the popup text

    # Display the map
    #m.save("map_gps/" + subdir_name + "/" + str(filename) + ".html")  # Save the map as an HTML file
    #m  # Display the map inline in Jupyter Notebook or simil
    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save("map_gps/" + subdir_name + "/" + str(filename) + ".png")

all_subdirs = os.listdir()
for subdir_name in all_subdirs: 
    if not os.path.isdir(subdir_name) or "Vehicle" not in subdir_name:
        continue 
    all_files = os.listdir(subdir_name + "/cleaned_csv/") 
    for some_file in all_files:  
        file_with_ride = pd.read_csv(subdir_name + "/cleaned_csv/" + some_file)
        longitudes = list(file_with_ride["fields_longitude"])
        latitudes = list(file_with_ride["fields_latitude"]) 
        if not os.path.isdir("map_gps/" + subdir_name):
            os.makedirs("map_gps/" + subdir_name)
        save_trajmap(longitudes, latitudes, subdir_name, some_file.replace(".csv", ""))

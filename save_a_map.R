# Čišćenje radne površine 

rm(list = ls()) 

# Uključivanje knjižnice trajr radi izračuna značajki putanja

library(trajr)

# Knjižnica mapview omogućuje vizualizaciju prostornih podataka sa ili bez pozadinske karte.

library(mapview) 

# Uključivanje knjižnice leaflet za prikaz podloge OpenStreetMap (OSM)

library(leaflet) 

# Uključivanje knjižnice sp za prostorne podatke

library(sp)

# Uključivanje knjižnice sf za prostorne značajke

library(sf)

args <- commandArgs(trailingOnly = TRUE)


# Get a list of directories in the current working directory
subdir_names <- list.dirs()
setwd(".")
# Iterate through the directories
for (subdir_name in subdir_names) {
  if (!file.info(subdir_name)$isdir || !grepl("Vehicle", subdir_name)) {
    next  # Skip if not a directory or if "Vehicle" is not in the name
  }
  
  # Get a list of files in the 'cleaned_csv' subdirectory of the current directory
  all_files <- list.files(path = file.path(subdir_name, "cleaned_csv"), full.names = TRUE)
   
  # Iterate through the files
  for (some_file in all_files) { 
    veh <- subdir_name 
    ride <- gsub(".csv", "", basename(some_file))
    
    arg1 <- paste(veh, "//cleaned_csv//", ride, ".csv", sep = "")
    arg2 <- paste(".//traj_GPS//", gsub("./", "", veh), "//", ride, ".png", sep = "")
    
    # Čitanje podataka iz .csv datoteke u obliku podatkovnog okvira
    print(arg1)
    print(arg2)
    data_traj <- read.csv(arg1, header = TRUE, sep = ',')   
    
    # Prikaz podataka na podlozi OpenStreetMap (OSM)
    
    # Naredba print(m) osigurava da se kreirana karta prikaže u konzoli prilikom izvršavanja skripte.
    
    m <- leaflet() %>%
      addTiles() %>%# koristi se zadana pozadinska karta s OpenStreetMap pločicama (engl. tiles)
      
      addPolylines(
        lng = data_traj[,"fields_longitude"], 
        lat = data_traj[,"fields_latitude"], 
        col = "red" 
      ) %>%  
      
      print(m)
    m
    # Spremanje slike karte u .png datoteku funkcijom mapshot
    
    # Knjižnica mapview pruža funkciju mapshot za spremanje slike karte u slikovnu datoteku. 
    
    # Izvor podataka o načinima spremanja slike karte u R-u:
    # https://stackoverflow.com/questions/31336898/how-to-save-leaflet-in-r-map-as-png-or-jpg-file
    
    mapshot(m, file = arg2)
  }
}


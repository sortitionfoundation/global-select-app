# Random global location selection

This project is intended to select locations around the globe randomly , by these locations we can get the number of community convinent for [Global Assembly](https://globalassembly.org).
## Background

To achieve the random selection we used a python script (global-select-admin-centroids.py) to compute against the world population obtained from  [NASA](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-admin-unit-center-points-population-estimates-rev11/data-download).

## Installation

To make installation ypu will have to:

- Clone the [repo](https://github.com/GlobalAssembly/global-select-app.git) 

- Download the  global population datasets [here](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-admin-unit-center-points-population-estimates-rev11/data-download) (You may have to create an account with them)

- Downlaod the UN country file [here](https://api.map.globalassembly.org/resources/country-code-UN-Region-max.csv) 

- After the installation you have to change the root (global_pop_admin_centroids_file_root) and (global_pop_output_file_root) to reflect where you have your global population datasets

## Executing locally

1. Running the script locally you can use

```
python3 global-select-admin-centroids.py
```

2. As the script is running it will update you with which it is reading from datasets

3. The results will be available in the file called (gobal-ca-people-points.csv)

## Serving the results through an API

By using an [express](http://expressjs.com) app , you can expose different endpoints to interacts with the script and its results
here are the sets to follow:

1. Have a server ready with node installed
2. Clone the [repo](https://github.com/GlobalAssembly/global-select-app.git)
3. Have the Global population datasets on server. You can find them [here](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-admin-unit-center-points-population-estimates-rev11/data-download)

4. Make changes in the script in reflect the root location of your datasets.

5. Server your express app (using your convinient ways)

6. There are various endpoints we have (eg: /run ( to execute the script) or /read ( to read the results ))

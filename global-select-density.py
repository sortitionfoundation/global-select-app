# Global selection code....the beginning
#
# Dec 2020 by Brett Hennig and ....
#

import csv
import random

# Settings/input

# must download data and put it here of course...
global_pop_den_file_name = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/stats/gpw-v4-population-density-rev11_2020_1_deg_asc/gpw_v4_population_density_rev11_2020_1_deg.asc"
num_points = 1000
# output file:
google_out_file_name = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/data-points/sample-data-points-google.csv"


# Read in the database from
#
# NEW: https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-adjusted-to-2015-unwpp-country-totals-rev11/data-download
# or
#   https://ghsl.jrc.ec.europa.eu/ (Paul's suggestion)
#

global_pop_den_file = open( global_pop_den_file_name, 'r' )
line1 = global_pop_den_file.readline()
line2 = global_pop_den_file.readline()
line3 = global_pop_den_file.readline()
line4 = global_pop_den_file.readline()
line5 = global_pop_den_file.readline()
line6 = global_pop_den_file.readline()
lines = global_pop_den_file.readlines()
point = 0
points = []
densities = []
for y_coord, aline in enumerate( lines ):
	latitude = 90 - y_coord
	aline = aline.strip()
	pop_dense_vals = aline.split(" ")
	#print(pop_dense_vals)
	for x_coord, pop_dense_val in enumerate( pop_dense_vals ):
		longitude = x_coord - 180
		if pop_dense_val != '-9999':
			#points.append( {'latitude' : latitude, 'longitude' : longitude, 'pop_dense_val' : pop_dense_val})
			points.append( {'latitude' : latitude, 'longitude' : longitude } )
			pop_dense_val_float = float( pop_dense_val )
			densities.append( pop_dense_val_float )
			#print( "{}, {}, {}".format(latitude, longitude, pop_dense_val))
			point += 1

#print(global_pop_file_reader.fieldnames)

		
#print(points)
print("Finished reading in population data file... points = {}".format(point))

# Select num_points points - population/density weighted?

#selected = random.sample(points, num_points)
selected = random.choices(points, weights=densities, k=num_points)
print("Randomly selected {} points from data.".format(num_points))

# output them for google map input
out_file_google = open(google_out_file_name, "w")
out_file_google.write("latitude, longitude, pop_dense_val\n") # Google maps needs this...
for pt in selected:
	#print(pt)
	out_file_google.write(str(pt['latitude'])+", "+str(pt['longitude'])+'\n')

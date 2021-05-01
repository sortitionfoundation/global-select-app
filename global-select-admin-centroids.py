# Global selection code....the second attempt - using admin centroisd
#
# April 2020 by Brett Hennig and ....
#

import csv, random, math

# Settings/input

# must download data and put it here of course...
global_pop_admin_centroids_file_root = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/data-points/GPWv4/gpw-v4-admin-unit-center-points-population-estimates-rev11_global_csv/"
global_pop_output_file_root = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/data-points/"
'''
#must change root above to use these...
global_pop_admin_centroids_files = [ "gpw-v4-admin-unit-center-points-population-estimates-rev11_oceania_csv/gpw_v4_admin_unit_center_points_population_estimates_rev11_oceania.csv",
		"gpw-v4-admin-unit-center-points-population-estimates-rev11_africa_csv/gpw_v4_admin_unit_center_points_population_estimates_rev11_africa.csv",
		"gpw-v4-admin-unit-center-points-population-estimates-rev11_south_america_csv/gpw_v4_admin_unit_center_points_population_estimates_rev11_south_america.csv",
		"gpw-v4-admin-unit-center-points-population-estimates-rev11_asia_csv/gpw_v4_admin_unit_center_points_population_estimates_rev11_asia.csv" ]
'''
global_pop_admin_centroids_files = [
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_global.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_midwest.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_northeast.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_south.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_west.csv"
		]
num_points = 100
# output file:
google_out_file_name = global_pop_output_file_root + "100-person-oceania-sample-data-points-google.csv"


# Read in the database from
#
# https://sedac.ciesin.columbia.edu/data/set/gpw-v4-admin-unit-center-points-population-estimates-rev11
#
# or could use pop density
# or could use: https://ghsl.jrc.ec.europa.eu/ghs_pop2019.php (but this is based on GPWv4)

# this just counts the total pop - did this once then put in line below
'''
total_pop = 0
for file_name in global_pop_admin_centroids_files:
	print("Reading in: " + file_name)
	file_handle = open(global_pop_admin_centroids_file_root + file_name, 'r')
	file_reader = csv.DictReader(file_handle)
	for row in file_reader:
		total_pop += int(row[ "UN_2020_E" ])
	file_handle.close()
	print("Total (file) pop = {}".format(total_pop))
'''
total_pop = 7758177449
print("Total pop = {}".format(total_pop))
	

# Select num_points points - population/density weighted?
selected_nums = []
for i in range(num_points):
	selected_nums.append(random.randint(1, total_pop))

print("Randomly selected {} people from total pop.".format(len(selected_nums)))
selected_nums.sort()

selected_list_count = 0
total_pop = 0
selected_people = []
for file_name in global_pop_admin_centroids_files:
	print("Reading in: " + file_name)
	file_handle = open(global_pop_admin_centroids_file_root + file_name, 'r')
	file_reader = csv.DictReader(file_handle)
	for row in file_reader:
		pop_row = int(row[ "UN_2020_E" ])
		# there might be more than one person we want in here!! the next number could even be the same number...
		while selected_list_count < num_points and selected_nums[selected_list_count] > total_pop and selected_nums[selected_list_count] <= total_pop + pop_row:
			#found a person we want!
			#print(selected_list_count, selected_nums[selected_list_count], total_pop, total_pop + pop_row)
			place_name = row["NAME1"] + ' - ' + row["NAME2"] + ' - ' + row["NAME3"]
			place_country = row["COUNTRYNM"]
			# throw a random offset into location based on its size, approximate as circle!
			orig_radius = math.sqrt(float(row["TOTAL_A_KM"])/math.pi)
			rand_radius_km = random.random()*orig_radius
			# see: http://www.edwilliams.org/avform147.htm#LL
			# for what is going on here - but basically just displacing the point
			# a little bit, depending on the size of the admin area
			# rand_radius_radians (distance units in formula are weird, 1 Nautical mile = 1852 m)
			rrr = (math.pi/(180*60))*1000*rand_radius_km/1852.0
			tc = random.random()*2*math.pi
			lat1 = math.radians(float(row["CENTROID_Y"]))
			lon1 = math.radians(float(row["CENTROID_X"]))
			lat2 = math.asin(math.sin(lat1)*math.cos(rrr)+math.cos(lat1)*math.sin(rrr)*math.cos(tc))
			lon2 = (lon1-math.asin(math.sin(tc)*math.sin(rrr)/math.cos(lat2))+math.pi)%(2*math.pi) - math.pi
			rand_lat_deg = math.degrees(lat2)
			rand_lon_deg = math.degrees(lon2)
			distance = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2))
			#print(row["TOTAL_A_KM"], orig_radius, distance)
			#print(row["CENTROID_Y"], row["CENTROID_X"],rand_lat_deg,rand_lon_deg)
			selected_people.append( [ rand_lat_deg, rand_lon_deg, place_name, place_country ] )
			selected_list_count += 1
		total_pop += pop_row
	file_handle.close()
print("Total pop (post selection) = {}".format(total_pop))


# output them for google map input
out_file_google = open(google_out_file_name, "w")
out_file_google.write("latitude, longitude, name, country\n") # Google maps needs this...
for person in selected_people:
	out_file_google.write(",".join(str(x) for x in person) + "\n")
out_file_google.close()

# Global selection code....the second attempt - using admin centroids
#
# April 2020 by Brett Hennig and ....
#

import csv, random, math

# Settings/input

# must download data and put it here of course...
global_pop_admin_centroids_file_root = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/data-points/GPWv4/gpw-v4-admin-unit-center-points-population-estimates-rev11_global_csv/"
global_pop_output_file_root = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/data-points/"
global_pop_admin_centroids_files = [
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_global.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_midwest.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_northeast.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_south.csv",
		"gpw_v4_admin_unit_center_points_population_estimates_rev11_usa_west.csv"
		]
un_region_country_count_file = global_pop_output_file_root + "country-code-UN Region-max.csv"

# TESTing area (oceania):
#global_pop_admin_centroids_file_root = "/Users/bsh/brett/sortition/foundation/projects-events/Stratification-Services/Global CA/data-points/GPWv4/gpw-v4-admin-unit-center-points-population-estimates-rev11_oceania_csv/"
#global_pop_admin_centroids_files = ["gpw_v4_admin_unit_center_points_population_estimates_rev11_oceania.csv"]
#total_pop = 42131508
# Testing non-US only
#total_pop = 7424623670
total_pop = 7758177449
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





# from https://en.wikipedia.org/wiki/United_Nations_Regional_Groups
class un_region():
	def __init__(self, region_name, max_count):
		self.region_name = region_name
		self.max_region_count = max_count
		self.region_count = 0
		self.countries = {}
		#self.people = []
		
	def add_country_to_region(self, country_code, country_max):
		self.countries[ country_code ] = { "country_max" : country_max, "country_people" : [] }
	
	def add_person_to_region(self, person):
		self.region_count += 1
		#self.people.append( person )
		#self.countries[ person["country_iso"] ][ "country_count" ] += 1
		self.countries[ person["country_iso"] ][ "country_people" ].append( person )
		
	def write_country_summary(self, out_file_google):
		for country_key, country_vals in self.countries.items():
			country_count = len(country_vals[ "country_people" ])
			if country_count != 0:
				out_file_google.write( country_key + "," + str(country_vals[ "country_max" ]) + "," + str(country_count) + "\n" )
		return self.region_name + "," + str(self.max_region_count) + "," + str(self.region_count) + "\n"
		
	def write_people(self):
		file_output = ''
		for country_vals in self.countries.values():
			for person in country_vals["country_people"]:
				file_output += ",".join(str(x) for x in person.values()) + "\n"
		return file_output
		
	def delete_above_max(self):
		# first check country maxs
		num_deleted = 0
		for country_key, country_vals in self.countries.items():
			country_count = len(country_vals[ "country_people" ])
			if country_count > country_vals[ "country_max" ]:
				#print(country_count)
				num_to_delete = country_count - country_vals[ "country_max" ]
				print("country {} above max, delete {}".format(country_key, num_to_delete))
				# delete num_to_delete
				# chose who to delete
				to_delete = set(random.sample(range(country_count), num_to_delete))
				# delete them
				country_vals[ "country_people" ] = [x for i,x in enumerate(country_vals[ "country_people" ]) if not i in to_delete]
				num_deleted += num_to_delete
				self.region_count -= num_to_delete
				#print(len(country_vals[ "country_people" ]))
			#region_count += len(country_vals[ "country_people" ])
		if self.region_count > self.max_region_count:
			#print(region_count)
			num_to_delete = self.region_count - self.max_region_count
			print("region {} above max, delete {}".format(self.region_name, num_to_delete))
			# delete num_to_delete
			to_delete = set(random.sample(range(self.region_count), num_to_delete))
			for country_key, country_vals in self.countries.items():
				orig_len = len(country_vals[ "country_people" ])
				country_vals[ "country_people" ] = [x for i,x in enumerate(country_vals[ "country_people" ]) if not i in to_delete]
				to_delete = [x - orig_len for x in to_delete]
				#new_region_count += len(country_vals[ "country_people" ])
			#print(new_region_count)
			num_deleted += num_to_delete
			self.region_count -= num_to_delete
		return num_deleted
	
	def replacement( self, person ):
		if self.region_count < self.max_region_count:
			country = self.countries[ person["country_iso"] ]
			if len(country[ "country_people" ]) < country[ "country_max" ]:
				country[ "country_people" ].append(person)
				self.region_count += 1
				return 1
			else:
				#print("failed to replace in {} as {} of {}".format(person["country_iso"], len(country[ "country_people" ]), country[ "country_max" ]))
				return 0
		else:
			#print("failed to replace in {} as {} of {}".format(self.region_name, self.region_count, self.max_region_count))
			return 0

	def get_person(self, x):
		total_country_count = 0
		for country_key, country_vals in self.countries.items():
			country_count = len(country_vals[ "country_people" ])
			if x >= total_country_count and x < total_country_count + country_count:
				return country_vals[ "country_people" ][x - total_country_count]
			total_country_count += country_count
		print("error - got to country list end {}".format(x))
		
		
class ca_people():
	name_fields = ["NAME1", "NAME2", "NAME3", "NAME4", "NAME5", "NAME6"]
	# calculated this once from above
	total_pop = 0 #7758177449
	#total_pop = 42131508
	#num_points = 0 #100

	def __init__(self, total_pop, num_points):
		ca_people.total_pop = total_pop
		self.num_points = num_points
		self.regions = {
			"Africa Group" : un_region("Africa Group", 16),
			"Asia and the Pacific Group" : un_region("Asia and the Pacific Group", 59),
			"Eastern European Group" : un_region("Eastern European Group", 5),
			"Latin American and Caribbean Group" : un_region("Latin American and Caribbean Group", 9),
			"Western European and Others Group" : un_region("Western European and Others Group", 12)  }
		print("Total pop = {}".format(ca_people.total_pop))
		# first value is max, second is count
		#un_region_count = {"Africa Group" : [16, 0] "Asia and the Pacific Group" : [59, 0], "Eastern European Group" : [5, 0], "Latin American and Caribbean Group" : [9, 0], "Western European and Others Group" : [12, 0]}
		# read in region and country count
		un_region_file_handle = open(un_region_country_count_file, 'r')
		un_region_file_reader = csv.DictReader(un_region_file_handle)
		self.country_region = {}
		for row in un_region_file_reader:
			self.regions[ row["un_region"] ].add_country_to_region( row["country_code"], int(row["country_max"]) )
			self.country_region[row["country_code"]] = row["un_region"]

		# Select num_points points - population/density weighted?
		self.selected_nums = []
		# grab same number of backups as well - could be the same!
		for i in range(self.num_points):
			self.selected_nums.append(random.randint(1, ca_people.total_pop))

		print("Randomly selected {} people from total pop.".format(len(self.selected_nums)))
		self.selected_nums.sort()		
		self.count_selected_people = 0


	def grab_people_in_admin_area(self, pop_count, row):
		pop_row = int(row[ "UN_2020_E" ])
		while self.count_selected_people < self.num_points and self.selected_nums[self.count_selected_people] > pop_count and self.selected_nums[self.count_selected_people] <= pop_count + pop_row:
			#found a person we want!
			#print(selected_list_count, people_nums[selected_list_count], total_pop, total_pop + pop_row)
			place_name = ''
			for nm in ca_people.name_fields:
				if row[ nm ] != "NA":
					if place_name != '':
						place_name += ' -- '
					place_name += row[nm].strip()
			place_country = row["COUNTRYNM"].strip()
			place_country_iso = row["ISOALPHA"]
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
			#distance = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2))
			#print(row["TOTAL_A_KM"], orig_radius, distance)
			#print(row["CENTROID_Y"], row["CENTROID_X"],rand_lat_deg,rand_lon_deg) 
			# add to counts for country and region
			if place_country_iso in self.country_region.keys():
				person_region = self.country_region[place_country_iso]
			else:
				if place_country_iso == "MNP": # Northern Mariana Islands (US)
					place_country_iso = "USA"
					person_region = "Western European and Others Group"
				elif place_country_iso == "HKG" or place_country_iso == "TWN": # China/claimed by China
					place_country_iso = "CHN"
					person_region = "Asia and the Pacific Group"
				else:
					print("Error {} not in country-region map.".format(place_country_iso))
					person_region = "Not in map"
			person = { "latitude" : rand_lat_deg,
					"longitude" : rand_lon_deg,
					"name" : place_name,
					"country" : place_country,
					"country_iso" : place_country_iso,
					"un_region" : person_region }
			if person_region != "Not in map":
				self.regions[ person_region ].add_person_to_region( person )
			self.count_selected_people += 1
			#self.selected_people.append( person )

	'''	
	def selected_people_min_dist(self):
		# this initialises list with a big number...
		selected_people_min_dist = [1e15]*ca_people.num_points
		for p1_num in range(len(self.selected_people)-1):
			lat1 = math.radians(self.selected_people[p1_num]["latitude"])
			lon1 = math.radians(self.selected_people[p1_num]["longitude"])
			for p2_num in range(p1_num + 1 , len(self.selected_people)):
				lat2 = math.radians(self.selected_people[p2_num]["latitude"])
				lon2 = math.radians(self.selected_people[p2_num]["longitude"])
				distance = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2))
				# to km
				distance = 1852*distance*180*60/(1000*math.pi)
				#print(p1_num, p2_num, distance)
				if distance < selected_people_min_dist[p1_num]:
					selected_people_min_dist[p1_num] = distance
				if distance < selected_people_min_dist[p2_num]:
					selected_people_min_dist[p2_num] = distance
		self.average_dist = sum(selected_people_min_dist)/ca_people.num_points
		print("Average minimum distance between points = {}".format(self.average_dist))
	'''
		
	def selected_people_print(self):
		# output them for google map input
		out_file_google = open(google_out_file_name, "w")
		#out_file_google.write(",".join(str(x) for x in self.selected_people[0].keys()) + "\n") # Google maps needs this...
		#for person in self.selected_people:
		#	out_file_google.write(",".join(str(x) for x in person.values()) + "\n")
		file_output = "latitude, longitude, name, country, country_iso, un_region\n"
		for region in self.regions.values():
			file_output += region.write_people()
		out_file_google.write( file_output )
		#out_file_google.write("Average minimum distance between points = {}\n".format(self.average_dist))
		# print country and region counts as well...
		out_file_google.write("country_iso, country_max, country_count\n")
		region_summary = ''
		for region in self.regions.values():
			region_summary += region.write_country_summary( out_file_google )
		out_file_google.write( "region_name, region_max, region_count\n" + region_summary )
		out_file_google.close()
	
	def get_person(self, x):
		total_region_count = 0
		for region in self.regions.values():
			if x >= total_region_count and x < total_region_count + region.region_count:
				#print(region.region_name, x, total_region_count, total_region_count + region.region_count, x - total_region_count )
				return region.get_person( x - total_region_count )
			total_region_count += region.region_count
		print("error - got to region list end {}".format(x))
	
	def replace_above_max(self, gca_backups):
		num_deleted = 0
		# for each region delete random people above max
		for region in self.regions.values():
			num_deleted += region.delete_above_max()
		print("delete total {}".format(num_deleted))
		self.count_selected_people -= num_deleted
		# then replace these deleted from the pool
		#replacements = random.sample(range(ca_people.num_points - num_deleted), num_deleted)
		replacements = random.sample(range(gca_backups.num_points), int(gca_backups.num_points/2))
		#print(replacements)
		success_replace = 0
		for x in replacements:
			person = gca_backups.get_person(x)
			#print(person["un_region"])
			success_replace += self.regions[ person["un_region"] ].replacement( person )
			if success_replace == num_deleted:
				break;
		print("successfully replaced {} people".format(success_replace))
			

gca_people = ca_people(total_pop, num_points)
print("And backup people...")
gca_backups = ca_people(total_pop, num_points)

pop_count = 0
for file_name in global_pop_admin_centroids_files:
	print("Reading in: " + file_name)
	file_handle = open(global_pop_admin_centroids_file_root + file_name, 'r')
	file_reader = csv.DictReader(file_handle)
	for row in file_reader:	
		pop_row = int(row[ "UN_2020_E" ])
		# there might be more than one person we want in here!! the next number could even be the same number...
		gca_people.grab_people_in_admin_area(pop_count, row)
		gca_backups.grab_people_in_admin_area(pop_count, row)
		pop_count += pop_row
	file_handle.close()
print("Total pop (post selection) = {}".format(pop_count))

# work out how many people in each UN region

# calculate the distance to the closet other point for every point, and sum these minimum distances
#gca_people.selected_people_min_dist()

gca_people.replace_above_max(gca_backups)

gca_people.selected_people_print()


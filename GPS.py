import csv
import webbrowser
import math

class School():
    #receive a dictionary corresponding to a row
    def __init__(self, data):
        self.id = int(data['School_ID'])
        self.name = data['Short_Name']
        self.network = data['Network']
        self.address = data['Address']
        self.zip = data['Zip']
        self.phone = data['Phone']
        self.grades = data['Grades'].split(',')
        self.location = Coordinate.fromdegrees(data['Lat'],data['Long'])

    def open_website(self):
        return webbrowser.open_new_tab('http://schoolinfo.cps.edu/schoolprofile/SchoolDetails.aspx?SchoolId={}'.format(self.id))

    def distance(self,coord):
        return Coordinate.distance(self.location,coord)

    def full_address(self):
        return '{} \nChicago, IL {}'.format(self.address, self.zip)


class Coordinate(School):
    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    @classmethod
    def fromdegrees(cls, latitude, longitude):
        return cls(latitude,longitude)

    #maybe try and find a way to call from constructor instead of down here.
    def distance(self,coord):
        lat1, long1, lat2, long2 = self.degrees_to_radians()[0], self.degrees_to_radians()[1], coord.degrees_to_radians()[0], coord.degrees_to_radians()[1]
        d = 2*3961*math.asin(math.sqrt(math.sin((lat2 - lat1)/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin((long2-long1)/2)**2))
        return d

    def as_degree(self):
        return(self.latitude,self.longitude)

    def show_map(self):
        return webbrowser.open_new_tab('http://maps.google.com/maps?q={},{}'.format(self.latitude,self.longitude))

    def degrees_to_radians(self):
        return ((self.latitude*(math.pi/180), self.longitude*(math.pi/180)))


class CSV(School):
    def __init__(self, filename):
        self.schools = []
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.schools.append(School(row))

    def nearby_schools(self, coord, radius=1.0):
        return [i.name for i in self.schools if i.location.distance(coord) < radius]

    def get_schools_by_grade(self, *grades):
        return [i.name for i in self.schools if ''.join(grades) in i.grades]


    def get_schools_by_network(self, network):
        return [i.name for i in self.schools if ''.join(network) in i.network]






cps = CSV('schools.csv') #list of all instances

for i in cps.schools:
    print(i.name)

for s in cps.schools:
    if s.name.startswith('OR'):
        print(s.name)

ace_tech = cps.schools[1]

the_bean = Coordinate.fromdegrees(41.8821512, -87.6246838)

print(ace_tech.location.distance(the_bean))


print(cps.nearby_schools(the_bean, radius=.5))
print(cps.get_schools_by_grade('K'))
print(cps.get_schools_by_network('Contract'))

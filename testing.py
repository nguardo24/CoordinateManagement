# Script used to test the functionality of the two classes

# Import the classed from the module

from coordinates import CoordinateFormatter, CoordinateTransformer

# Instantiate the objets (formatter and transformer)

coordinate_formatter = CoordinateFormatter()

coordinate_transformer = CoordinateTransformer(epsg_from=5347, epsg_to=5340)

# The example coordinates

coordinates = ((5459692.632, 6111523.997), 
               (5460335.423, 6111569.977), 
               (5460506.581, 6111795.698),
               (5460536.369, 6111931.428))

# First, we transform the projected coordinates into decimal degrees

coordinates_transformed = coordinate_transformer.transform_coordinates(coordinates)

# Then, we loop over the pairs (x, y) and format the DD coordinates into DMS coordinates
for x, y in coordinates_transformed:
    print(coordinate_formatter.londd_to_londms(x), coordinate_formatter.latdd_to_latdms(y), sep="\t")
import re

import numpy as np
from pyproj import CRS, Transformer

class CoordinateFormatter:
    
    @staticmethod
    def dd_to_dms(coordinate: float) -> str:
        """
        Convert a coordinate value expressed as decimal degrees into sexagesimal degrees
        
        Parameters
        ----------
        coordinate : float
            Coordinate to be converted
        
        Returns
        -------
        dms_coord : str
            Coordinate expressed in sexagesimal degrees
        """
        degrees = abs(int(coordinate))
        minutes = (abs(coordinate) % 1) * 60
        seconds = (minutes % 1) * 60
        
        dms_coord = f"{degrees}°{int(minutes)}'{seconds:.5f}\""

        return dms_coord
    
    def dms_to_dd(self, coordinate: str) -> float:
        """
        Convert a coordinate value expressed as sexagesimal degrees into decimal degrees
        
        Parameters
        ----------
        coordinate : str
            Coordinate to be converted
        
        Returns
        -------
        dd_coord : float
            Coordinate expressed in decimal degrees. Depending on the hemisphere, it will be a positive (N, E) or negative (S, W) number. 
        """
        pattern = "(\d{1,3})°\s?([0-5]?[0-9])'\s?([0-5]?[0-9].?\d*)\"\s?([NSEW])"
        
        match = re.search(pattern, coordinate)
        
        degrees = match.group(1)
        minutes = match.group(2)
        seconds = match.group(3)
        direction = match.group(4)
        
        dd_coord = float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)
        
        return dd_coord if direction in ["N", "E"] else -dd_coord
        
    def londd_to_londms(self, coordinate: float) -> str:
        """
        Convert longitude coordinates expressed in decimal degrees into sexagesimal degrees
        
        Parameters
        ----------
        coordinate : float
            Longitude coordinate to be converted
        
        Returns
        -------
        londms : str
            Longitude expressed in sexagesimal degrees
        """
        assert -180 <= coordinate <= 180, "Longitude should be between -180 and 180 degrees"
        
        direction = "E" if coordinate > 0 else "W"
        
        londms = f"{self.dd_to_dms(coordinate)}{direction}"

        return londms
    
    def latdd_to_latdms(self, coordinate: float) -> str:
        """
        Convert latitude coordinates expressed in decimal degrees into sexagesimal degrees.
        
        Parameters
        ----------
        coordinate : float
            Latitude coordinate to be converted
        
        Returns
        -------
        latdms : str
            Latitude expressed in sexagesimal degrees
        """
        assert -90 <= coordinate <= 90, "Latitude should be between -90 and 90 degrees"
        
        direction = "N" if coordinate > 0 else "S"
        
        latdms = f"{self.dd_to_dms(coordinate)}{direction}"
        
        return latdms

class CoordinateTransformer:
    
    def __init__(self, epsg_from: str | int | CRS, epsg_to: str | int | CRS):
        """
        The constructor method of the class
        """
        self.transformer = Transformer.from_crs(epsg_from, epsg_to, always_xy=True)
        
    def transform_coordinates(self, coordinates: list | tuple | np.ndarray) -> np.ndarray:
        """
        Transform coordinates between origin and destination coordinate systems
        
        Parameters 
        ----------
        coordinates : list | tuple | np.ndarray
            The coordinates to be transformed
        
        Returns
        -------
        transformed_coordinates : np.ndarray
            A 2D numpy array with the x,y coordinate pairs transformed 
        """
        transformed_coordinates = np.array(list(self.transformer.itransform(coordinates)))
        
        return transformed_coordinates
    
    def transform_pair(self, x: int | float, y: int | float, z: int | float = 0) -> tuple:
        """
        Transform individual pair of coordinates between origin and destination coordinate systems
        
        Parameters
        ----------
        x : int | float
            Longitude coordinate
        y : int | float
            Latitude coordinate
        z : int | float
            Vertical/altitude coordinate (optional)
        
        Returns
        -------
        transformed_pair : tuple
            Tuple containing the transformed pair
        """
        transformed_pair = self.transformer.transform(x, y, z)
        
        return transformed_pair

if __name__ == "__main__":
    
    # Show an example of the use
    
    formatter = CoordinateFormatter()
    transformer = CoordinateTransformer("4326", CRS.from_epsg(5348))

    coordinates = np.array([
            [
              -57.60365758800924,
              -35.4968257854251
            ],
            [
              -57.51025409413067,
              -35.609455111208554
            ]
        ])
    
    # print(conversor.latdd_to_latdms(0.5345))
    
    print(formatter.dms_to_dd("33°41'12.2\"S"))
    print(formatter.dms_to_dd("68° 01' 38.44\" W"))
    print(formatter.dms_to_dd("68° 01' 08.44\" W"))
    
    print(formatter.latdd_to_latdms(-34.7393611), formatter.londd_to_londms(112.12), sep="\n")
    
    transformed_coordinates = transformer.transform_coordinates(coordinates)
    
    print(transformed_coordinates)
# -*- coding: utf-8 -*-
from typing import Tuple

import numpy as np


########################################################################################################################
class MoreTransfers:
    """
    TODO Eventually combine with other coord transfers and re-organize.
    """
    def __int__(self):
        pass

    ####################################################################################################################
    @staticmethod
    def geodetic2ecef(lat: float, lon: float, alt: float,
                      deg: bool = True) -> Tuple[float, float, float]:
        """
        Point

        input:
        -----
        lat, lon (degrees)
        alt (altitude, meters)    [0, Infinity)
        deg    degrees input/output  (False: radians in/out)

        output: ECEF x,y,z (meters)
        """
        aParam = 6378137.  # semi-major axis [m]
        fParam = 1 / 298.2572235630  # flattening
        bParam = aParam * (1 - fParam)  # semi-minor axis
        if deg:
            lat = lat * np.pi / 180
            lon = lon * np.pi / 180

        with np.errstate(invalid='ignore'):
            # need np.any() to handle scalar and array cases
            if np.any((lat < -np.pi / 2) | (lat > np.pi / 2)):
                raise ValueError('-90 <= lat <= 90')

            if np.any((lon < -np.pi) | (lon > 2 * np.pi)):
                raise ValueError('-180 <= lat <= 360')

            if np.any(np.asarray(alt) < 0):
                raise ValueError('altitude  [0, Infinity)')
        # radius of curvature of the prime vertical section
        N = MoreTransfers.get_radius_normal(lat)
        # Compute cartesian (geocentric) coordinates given  (curvilinear) geodetic
        # coordinates.
        x = (N + alt) * np.cos(lat) * np.cos(lon)
        y = (N + alt) * np.cos(lat) * np.sin(lon)
        z = (N * (bParam / aParam) ** 2 + alt) * np.sin(lat)

        return x, y, z

    ####################################################################################################################
    @staticmethod
    def get_radius_normal(lat_radians: float) -> float:
        """ Compute normal radius of planetary body"""

        aParam = 6378137.  # semi-major axis [m]
        fParam = 1 / 298.2572235630  # flattening
        bParam = aParam * (1 - fParam)  # semi-minor axis

        return aParam ** 2 / np.sqrt(aParam ** 2 * np.cos(lat_radians) ** 2 +
                                     bParam ** 2 * np.sin(lat_radians) ** 2)

    ####################################################################################################################
    @staticmethod
    def enu2uvw(east: float, north: float, up: float,
                lat0: float, lon0: float, deg: bool = True) -> Tuple[float, float, float]:
        if deg:
            lat0 = lat0 * np.pi / 180
            lon0 = lon0 * np.pi / 180

        t = np.cos(lat0) * up - np.sin(lat0) * north
        w = np.sin(lat0) * up + np.cos(lat0) * north

        u = np.cos(lon0) * t - np.sin(lon0) * east
        v = np.sin(lon0) * t + np.cos(lon0) * east

        return u, v, w

    ####################################################################################################################
    @staticmethod
    def enu2ecef(e1: float, n1: float, u1: float,
                 lat0: float, lon0: float, h0: float,
                 deg: bool = True) -> Tuple[float, float, float]:
        """
        ENU to ECEF

        inputs:
         e1, n1, u1 (meters)   east, north, up
         observer: lat0, lon0, h0 (degrees/radians,degrees/radians, meters)
        ell    reference ellipsoid
        deg    degrees input/output  (False: radians in/out)


        output
        ------
        x,y,z  [meters] target ECEF location                         [0,Infinity)
        """
        x0, y0, z0 = MoreTransfers.geodetic2ecef(lat0, lon0, h0, deg=deg)
        dx, dy, dz = MoreTransfers.enu2uvw(e1, n1, u1, lat0, lon0, deg=deg)

        return x0 + dx, y0 + dy, z0 + dz

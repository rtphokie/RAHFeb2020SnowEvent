import unittest
import simple_cache
from pprint import pprint
import struct
import matplotlib.colors as col
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
# try:
#   from mpl_toolkits.basemap import Basemap
# except:
  # !apt-get install libgeos-dev
  # !pip install https://github.com/matplotlib/basemap/archive/master.zip
  # %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import requests
import os
import logging
from pprint import pprint
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, filename='mapping.log',level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

# Constants
earth_radius_major = 6378137.000 # useful for more accurate rendering of Mercator and Lambert projections
earth_radius_minor = 6356752.3142
NWSLegend=[
           {'lower': 0.0, 'upper': 0.5, 'hexstring': '#04f7f1'},
           {'lower': 0.6, 'upper': 1.0, 'hexstring': '#36a5f7'},
           {'lower': 1.1, 'upper': 2.0, 'hexstring': '#3957f7'},
           {'lower': 2.1, 'upper': 3.0, 'hexstring': '#0003f1'},
           {'lower': 3.1, 'upper': 4.0, 'hexstring': '#6a03f4'},
           {'lower': 4.1, 'upper': 5.0, 'hexstring': '#b400f7'},
           {'lower': 5.1, 'upper': 6.0, 'hexstring': '#f401ef'},
           ]

# def hex2rgb(s):
#     return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:7], 16))
#
#     return struct.unpack('BBB', rgb.decode('hex'))

def NWScolormap(hexmap):
    sorted(hexmap, key=lambda i: i['lower'])
    cmap = colors.ListedColormap([x['hexstring'] for x in NWSLegend])
    boundaries = [x['lower'] for x in NWSLegend]
    norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)
    pprint(NWSLegend)

    def load_shapefile_from_git(m, dir, filename, drawbounds=False,
                                urlbase='https://raw.githubusercontent.com/rtphokie/RAHFeb2020SnowEvent/master'):
        for ext in ['dbf', 'shp', 'shx']:
            if not os.path.exists(f"{dir}/{filename}.{ext}"):
                if not os.path.exists(dir):
                    logging.info(f"directory {dir} created")
                    os.makedirs(dir)
                url = f'{urlbase}/{dir}/{filename}.{ext}'
                r = requests.get(url)
                logging.info(f'shapefile fetched from GIT {url}')
                with open(f"{dir}/{filename}.{ext}", 'wb') as f:
                    f.write(r.content)
                # else:
                logging.debug(f'using existing {ext} shapefile {filename}')
        m.readshapefile(f'{dir}/{filename}', filename, ax=ax, drawbounds=drawbounds)
        logging.info(f"{dir}/{filename} shapefile loaded")

    def draw_map_background(m, ax):
        ax.set_facecolor('#729FCF')
        m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
        m.drawcounties(ax=ax, color="darkgrey")
        m.drawstates(ax=ax, color='darkgrey')
        m.drawcountries(ax=ax)
        m.drawcoastlines(ax=ax)

    def draw_shapes(m, ax, dmas=['RALEIGH-DURHAM'], wfos=['RAH']):
        # m.readshapefile('https://github.com/rtphokie/RAHFeb2020SnowEvent/tree/master/dma_2008/DMAs', 'DMAs', ax=ax, drawbounds=False)
        load_shapefile_from_git(m, 'dma_2008', 'DMAs')
        load_shapefile_from_git(m, 'w_03mr20', 'w_03mr20')
        load_shapefile_from_git(m, 'NWS_actual', 'NWS_Actual_polygon', drawbounds=False)

        # m.readshapefile('mygeodata/NWS_Actual-polygon', 'NWS_Actual_polygon', ax=ax, drawbounds=True)
        # https://twitter.com/NWSRaleigh/status/1232344049568354307

        patches = {'0-0.5': [],
                   '2-3': [],
                   '3-4': [],
                   '4-5': [],
                   }

        for info, shape in zip(m.NWS_Actual_polygon_info, m.NWS_Actual_polygon):
            if info['Name'] in patches.keys():
                patches[info['Name']].append(Polygon(np.array(shape), True))
        pprint(patches)
        ax.add_collection(PatchCollection(patches['2-3'], edgecolor='k', linewidths=1., zorder=2))
        ax.add_collection(PatchCollection(patches['4-5'], edgecolor='k', alpha=0.5, linewidths=1., zorder=2))
        return
        wfos = []
        for info, shape in zip(m.w_03mr20_info, m.w_03mr20):
            # print(info)
            if info['WFO'] in wfos:
                # highlight county warning areas of interest
                # x, y = zip(*shape)
                wfos.append(Polygon(np.array(shape), True))
                # m.plot(x, y, marker=None, color='b', facecolor='b', alpha=0.5)
        ax.add_collection(wfos, edgecolor='k', linewidths=1., zorder=2)

        for info, shape in zip(m.DMAs_info, m.DMAs):
            if info['NAME'] in dmas:
                # highlight DMAs of interest
                x, y = zip(*shape)
                m.plot(x, y, marker=None, color='k')


def drawmap(res='h'):
    '''
    :param res:  [c]rude (faster), [l]ow, [h]ight(slower) [f]ull (really slow)
    :return:
    '''
    print ('drawing map')
    ax, fig, m = _drawmap(res)
    print ('drawing map')
    draw_shapes(m, ax)
    fig.text(0.5, 0.92, 'Feb 20, 2020 Snow Event', horizontalalignment='center')

    fig.savefig('foo.png')


@simple_cache.cache_it(filename="basemap.cache", ttl=120000)
def _drawmap(res, fillcontinents=True, counties="darkgrey", drawstates=True, drawcountries=True, drawcoastlines=True):
    '''
    This is expensive, caching results based on resolution
    :param res:
    :return:
    '''
    clat = 35.28  # NC center
    clon = -79.02
    wid = 1600000 / 2
    hgt = 900000 / 2
    logging.info(f"------------------------")
    m = Basemap(width=wid, height=hgt,
                rsphere=(earth_radius_major, earth_radius_minor),
                resolution=res, area_thresh=50., projection='lcc',
                lat_1=clat, lat_2=clat, lat_0=clat, lon_0=clon)
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#729FCF')
    m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
    if counties is not None: m.drawcounties(ax=ax, color=counties)
    if drawstates: m.drawstates(ax=ax, color='darkgrey')
    if drawcountries: m.drawcountries(ax=ax)
    if drawcoastlines: m.drawcoastlines(ax=ax)

    return ax, fig, m



def load_shapefile_from_git(m, ax, dir, filename, drawbounds=False, urlbase='https://raw.githubusercontent.com/rtphokie/RAHFeb2020SnowEvent/master'):
    for ext in ['dbf', 'shp', 'shx']:
        if not os.path.exists(f"{dir}/{filename}.{ext}"):
            if not os.path.exists(dir):
                logging.info(f"directory {dir} created")
                os.makedirs(dir)
            url = f'{urlbase}/{dir}/{filename}.{ext}'
            r = requests.get(url)
            logging.info(f'shapefile fetched from GIT {url}')
            with open(f"{dir}/{filename}.{ext}", 'wb') as f:
                f.write(r.content)
            # else:
            logging.debug(f'using existing {ext} shapefile {filename}')
    m.readshapefile(f'{dir}/{filename}', filename, ax=ax, drawbounds=drawbounds)
    logging.info(f"{dir}/{filename} shapefile loaded")


def draw_shapes(m, ax, dmas=['RALEIGH-DURHAM'], wfos=['RAH']):
    # m.readshapefile('https://github.com/rtphokie/RAHFeb2020SnowEvent/tree/master/dma_2008/DMAs', 'DMAs', ax=ax, drawbounds=False)
    load_shapefile_from_git(m, ax, 'dma_2008', 'DMAs')
    load_shapefile_from_git(m, ax, 'w_03mr20', 'w_03mr20')
    load_shapefile_from_git(m, ax, 'NWS_actual', 'NWS_Actual_polygon', drawbounds=False)

    patches = {'0-0.5': [],
               '2-3': [],
               '3-4': [],
               '4-5': [],
               }

    for info, shape in zip(m.NWS_Actual_polygon_info, m.NWS_Actual_polygon):
        if info['Name'] in patches.keys():
            patches[info['Name']].append(Polygon(np.array(shape), True))
    pprint(patches)
    ax.add_collection(PatchCollection(patches['2-3'], edgecolor='k', linewidths=1., zorder=2))
    ax.add_collection(PatchCollection(patches['4-5'], edgecolor='k', alpha=0.5, linewidths=1., zorder=2))

    collection_wfos = []
    for info, shape in zip(m.w_03mr20_info, m.w_03mr20):
        if info['WFO'] in wfos: # highlight county warning areas of interest
            collection_wfos.append(Polygon(np.array(shape), True))

    collection_dmas = []
    for info, shape in zip(m.DMAs_info, m.DMAs):
        if info['NAME'] in dmas: # highlight county warning areas of interest
            collection_dmas.append(Polygon(np.array(shape), True))

    ax.add_collection(PatchCollection(collection_wfos, edgecolor='k', facecolors='gray', alpha=0.2, linewidths=1., zorder=2))
    ax.add_collection(PatchCollection(collection_dmas, edgecolor='k', facecolors='gray', alpha=0.2, linewidths=1., zorder=3))

class MyTestCase(unittest.TestCase):
    def test_something(self):
        NWScolormap(NWSLegend)
        drawmap(res='i')


if __name__ == '__main__':
    unittest.main()

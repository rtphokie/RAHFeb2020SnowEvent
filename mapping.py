from shapely import geometry
# import simple_cache
#
# import struct
# import matplotlib.colors as col
# import numpy as np
# import matplotlib.pyplot as plt
# import geopandas
# from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import matplotlib.cm as cm

# uncomment below for running from Google Collaboratory containers
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
# from matplotlib.patches import PathPatch
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

NWSLegend={
'5.1-6': '#f401ef',
'4.1-5': '#b400f7',
'3.1-4': '#6b02f2',
'2.1-3': '#0002f1',
'1.1-2': '#335bf9',
'0.6-1': '#32a6fd',
'0-0.5': '#06f4f6',
}


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

# def draw_map_background(m, ax):
#     ax.set_facecolor('#729FCF')
#     m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
#     m.drawcounties(ax=ax, color="darkgrey")
#     m.drawstates(ax=ax, color='darkgrey')
#     m.drawcountries(ax=ax)
#     m.drawcoastlines(ax=ax)

# def draw_shapes(m, ax, dmas=['RALEIGH-DURHAM'], wfos=['RAH']):
#     # m.readshapefile('https://github.com/rtphokie/RAHFeb2020SnowEvent/tree/master/dma_2008/DMAs', 'DMAs', ax=ax, drawbounds=False)
#     load_shapefile_from_git(m, 'data/shapefiles/dma_2008', 'DMAs')
#     load_shapefile_from_git(m, 'data/shapefiles/w_03mr20', 'data/shapefiles/w_03mr20')
#     load_shapefile_from_git(m, 'NWS_actual', 'NWS_Actual_polygon', drawbounds=False)
#
#     # m.readshapefile('mygeodata/NWS_Actual-polygon', 'NWS_Actual_polygon', ax=ax, drawbounds=True)
#     # https://twitter.com/NWSRaleigh/status/1232344049568354307
#
#     patches = {'0-0.5': [],
#                '2-3': [],
#                '3-4': [],
#                '4-5': [],
#                }
#
#     for info, shape in zip(m.NWS_Actual_polygon_info, m.NWS_Actual_polygon):
#         if info['Name'] in patches.keys():
#             patches[info['Name']].append(Polygon(np.array(shape), True))
#     ax.add_collection(PatchCollection(patches['2-3'], edgecolor='k', linewidths=1., zorder=2))
#     ax.add_collection(PatchCollection(patches['4-5'], edgecolor='k', alpha=0.5, linewidths=1., zorder=2))
#     return
#     wfos = []
#     for info, shape in zip(m.w_03mr20_info, m.w_03mr20):
#         if info['WFO'] in wfos:
#             # highlight county warning areas of interest
#             # x, y = zip(*shape)
#             wfos.append(Polygon(np.array(shape), True))
#             # m.plot(x, y, marker=None, color='b', facecolor='b', alpha=0.5)
#     ax.add_collection(wfos, edgecolor='k', linewidths=1., zorder=2)
#
#     for info, shape in zip(m.DMAs_info, m.DMAs):
#         if info['NAME'] in dmas:
#             # highlight DMAs of interest
#             x, y = zip(*shape)
#             m.plot(x, y, marker=None, color='k')

def draw_wfo_dma_map(res='h', DMAs=['RALEIGH-DURHAM'], WFOs=['RAH']):
    '''
    :param res:  [c]rude (faster), [l]ow, [h]ight(slower) [f]ull (really slow)
    :return:
    '''
    ax, fig, m = _drawmap(res)
    draw_areas(m, ax, DMAs=DMAs, WFOs=WFOs)
    fig.text(0.5, 0.92, 'Feb 20, 2020 Snow Event', horizontalalignment='center')
    fig.savefig('foo.png')
    fig.show()

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
            logging.debug(f'using existing {ext} shapefile {filename}')
    m.readshapefile(f'{dir}/{filename}', filename, ax=ax, drawbounds=drawbounds)
    logging.info(f"{dir}/{filename} shapefile loaded")

def draw_shapes(m, ax):
    for forecaster in ['WRAL', 'WTVD']:
        shapefile = f'data/shapefiles/{forecaster}'
        shapename = forecaster
        m.readshapefile(f'{shapefile}/{shapename}', shapename, ax=ax, drawbounds=False)

def draw_areas(m, ax, DMAs=None, WFOs=None):
    # m.readshapefile('https://github.com/rtphokie/RAHFeb2020SnowEvent/tree/master/dma_2008/DMAs', 'DMAs', ax=ax, drawbounds=False)
    handles = {}

    # WFO shapefile from NOAA
     # https://matplotlib.org/3.3.1/tutorials/colors/colormaps.html
    column_of_interest='WFO'
    values_of_interest=WFOs
    shapefile = 'data/shapefiles/w_03mr20'
    shapename = 'w_03mr20'
    plot_shapes(ax, m, shapefile, shapename, column_of_interest,values_of_interest, handles,)


    # DMA shapefile from Harvard dataseet
    cmap = cm.get_cmap('rainbow') # https://matplotlib.org/3.3.1/tutorials/colors/colormaps.html
    column_of_interest='NAME'
    values_of_interest=DMAs
    dmashapedir = 'data/shapefiles/dma_2008'
    dmashapename = 'DMAs'
    plot_shapes(ax, m, 'data/shapefiles/dma_2008', 'DMAs', 'NAME',['RALEIGH-DURHAM'], handles,
                linewidths=4.0, colorbylistposition=False, labelcentroid=False)

    resultsdir = 'data/shapefiles/20200220NCSnowResults'
    resultsfile = '20200220NCSnowResults'
    categories = get_snowfall_categories(resultsdir, resultsfile)
    m.readshapefile(f'{resultsdir}/{resultsfile}', resultsfile, ax=ax, drawbounds=False)
    for category, bounds in categories.items():
        plot_shapes(ax, m, resultsdir, resultsfile, 'Name', category, {},
                    linewidths=0.0, facecolor=NWSLegend[category], alpha=1, colorbylistposition=False, labelcentroid=False)

def plot_shapes(ax, m, shapefile, shapename, column_of_interest,values_of_interest, handles,
                edgecolor='k', alpha=0.4, linewidths=0.5, fontsize=12, fontweight='bold',
                colorbylistposition=True, facecolor=None,
                labelcentroid=True, cmap='rainbow'):
    '''
    :param ax: axis
    :param cmap: colormap
    :param column_of_interest: column to look for matches in out of shapefile info database
    :param handles:  dictionary of mpatches, for building up a legend
    :param m: the map
    :param shapedir: directory for shapefiles
    :param shapename: shape name
    :param values_of_interest: value to look for in shapefile database
    :param edgecolor: color for polygon edge
    :param colorbylistposition: color code each polygon by its position in the passed list of values of interest within the specified colormap (default: True)
    :param alpha: light (0.0) or dark (1.0) to make the edge (default 0.4)
    :param linewidths: how thick to make the edge (default 0.5)
    :param labelcentroid: label each polygon at the inner centroid
    :param fontsize: how big to make the labels (default 12 point)
    :param fontweight: which font to use (default bold)
    :return: nothing, updates handles, m and x
    '''
    points = {}
    if  colorbylistposition:
        cmap = cm.get_cmap(cmap)
    load_shapefile_from_git(m, ax, shapefile, shapename, )
    m.readshapefile(f'{shapefile}/{shapename}', shapename, ax=ax, drawbounds=False)
    if len(values_of_interest) == 0:
        # if no values of interest were passed, use all unique values in the column of interest
        for v in m.__dict__[f"{shapename}_info"]:
            values_of_interest.append(v[column_of_interest])
        values_of_interest=list(set(values_of_interest))

    for info, shape in zip(m.__dict__[f"{shapename}_info"], m.__dict__[shapename]):
        if info[column_of_interest] in values_of_interest:  # highlight county warning areas of interest
            if labelcentroid:
                # gather all points related to this WFO (normalized to the portions shown on this map), for labeling at the centroid
                if info[column_of_interest] not in points.keys():
                    points[info[column_of_interest]] = []
                for a_tuple in shape:
                    points[info[column_of_interest]].append( geometry.Point(min(max(a_tuple[0], m.xmin), m.xmax), min(max(a_tuple[1], m.ymin), m.ymax)))
            collection_wfos = [Polygon(np.array(shape), True)]
            if colorbylistposition:
                facecolor = cmap((values_of_interest.index(info[column_of_interest]) + 1) / len( values_of_interest))  # pick from colormap based on position in list
            else:
                # no face color
                if facecolor is None:
                    facecolor = 'none'   # matplotlib uses keyword "none" for no color
            # ax.add_collection(PatchCollection(collection_wfos, facecolor='none', edgecolor='k', linewidths=4.0))
            ax.add_collection(PatchCollection(collection_wfos, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha, linewidths=linewidths))
            handles[info[column_of_interest]] = mpatches.Patch(color=facecolor, alpha=alpha, label=info[column_of_interest])

    # Label WFOs at the centroid
    if labelcentroid:
        for shapelabel in points.keys():
            poly = geometry.Polygon([[p.x, p.y] for p in points[shapelabel]])
            centroid = poly.centroid
            ax.text(centroid.x, centroid.y, shapelabel, fontsize=fontsize, fontweight=fontweight, ha='center', va='center', color='k')

def get_snowfall_categories(resultsdir, resultsfile):
    '''
    :param resultsdir: directory where NWS results map is stored
    :param resultsfile: NWS results shapefile name
    :return: list of categories
    '''
    categories = {}
    # Get snowfall range categories from NWS RAH final results map
    ax, fig, m = _drawmap('c', drawstates=True, drawcountries=True, drawcoastlines=True)
    m.readshapefile(f'{resultsdir}/{resultsfile}', str(resultsfile), ax=ax, drawbounds=False)
    for info, shape in zip(m.__dict__[f"{resultsfile}_info"], m.__dict__[resultsfile]):
        # iterate over resulting snowfall ranges from NWS RAH map
        lowerbound, upperbound = extract_range(info['Name'])
        categories[info['Name']] = {'lower': float(lowerbound), 'upper': float(upperbound)}
    return categories

def extract_range(s):
    if '-' in s:
        lowerbound, upperbound = s.split('-')
    else:
        lowerbound, upperbound = s, s
    return float(lowerbound), float(upperbound)


def plot_forecasts(ax, color, m, shapedir, shapename, snowupto):
    m.readshapefile(f'{shapedir}/{shapename}', str(shapename), ax=ax, drawbounds=False)
    for info, shape in zip(m.__dict__[f"{shapename}_info"], m.__dict__[shapename]):
        # if '-' in info['Name']:
        #     lowerbound, upperbound = info['Name'].split('-')
        # else:
        #     lowerbound, upperbound = info['Name'], info['Name']
        # if upperbound == str(snowupto):
        #     print(f"plotthis {info['Name']}")
            plot_shapes(ax, m, shapedir, shapename, 'Name', info['Name'], {},
                        linewidths=0.0, facecolor=color, colorbylistposition=False, labelcentroid=False)
from PyOphidia import cube

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import numpy as np

from pywps import configuration


def tropical_nights(dataset, output):
    cube.Cube.setclient(
        username=configuration.get_config_value('ophidia', 'username'),
        password=configuration.get_config_value('ophidia', 'password'),
        server=configuration.get_config_value('ophidia', 'server'),
        port=configuration.get_config_value('ophidia', 'port'))
    # Import source data (minimum temperature K)
    mintemp = cube.Cube(
        src_path=dataset,
        measure='temp2',
        import_metadata='yes',
        imp_dim='time',
        imp_concept_level='d',
        vocabulary='CF',
        hierarchy='oph_base|oph_base|oph_time',
        ncores=4,
        description='Min Temps'
    )
    # Identify the tropical nights
    tropicalnights = mintemp.apply(
        query="oph_predicate('OPH_FLOAT','OPH_INT',measure,'x-293.15','>0','1','0')"
    )
    # Count the number of tropical nights
    count = tropicalnights.reduce2(
        operation='sum',
        dim='time',
        concept_level='y',
    )
    # Plot the result
    firstyear = count.subset(subset_filter=1, subset_dims='time')
    data = firstyear.export_array(show_time='yes')
    lats = data['dimension'][0]['values'][:]
    lons = data['dimension'][1]['values'][:]
    var = data['measure'][0]['values'][:]
    var = np.reshape(var, (len(lats), len(lons)))
    clevs = np.arange(0, 371, 10)

    def _cartopy_plot():
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.set_global()
        plt.contourf(lons, lats, var, clevs, cmap=plt.cm.jet, transform=ccrs.PlateCarree())

    def _basemap_plot():
        fig = plt.figure(figsize=(15, 15), dpi=100)
        fig.add_axes([0.1, 0.1, 0.8, 0.8])
        map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        map.drawmeridians(np.arange(-180, 180, 30), labels=[0, 0, 0, 1])
        x, y = map(*np.meshgrid(lons, lats))
        cnplot = map.contourf(x, y, var, clevs, cmap=plt.cm.jet)
        map.colorbar(cnplot, location='right')
    _cartopy_plot()
    # _basemap_plot()
    # Save the plot by calling plt.savefig() BEFORE plt.show()
    plt.title('Tropical Nights (year 1980)')
    plt.savefig(output)
    plt.show()
    plt.close()

from PyOphidia import cube

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

from pywps import configuration


def tropical_nights(dataset, ouput):
    cube.Cube.setclient(
        username=configuration.get_config_value('ophidia', 'username'),
        password=configuration.get_config_value('ophidia', 'password'),
        server=configuration.get_config_value('ophidia', 'server'),
        port=configuration.get_config_value('ophidia', 'port'))
    # # Import source data (minimum temperature °K)
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
    # # Plot the result
    firstyear = count.subset(subset_filter=1, subset_dims='time')
    data = firstyear.export_array(show_time='yes')
    lat = data['dimension'][0]['values'][:]
    lon = data['dimension'][1]['values'][:]
    var = data['measure'][0]['values'][:]
    var = np.reshape(var, (len(lat), len(lon)))
    # cartopy plot
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_global()
    plt.contourf(lon, lat, var, 60, transform=ccrs.PlateCarree())
    # Save the plot by calling plt.savefig() BEFORE plt.show()
    plt.savefig(ouput)
    plt.title('Tropical Nights (year 1980)')
    plt.show()
    #
    # fig = plt.figure(figsize=(15, 15), dpi=100)
    # # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    #
    # map = Basemap(
    #     projection='cyl',
    #     llcrnrlat=-90,
    #     urcrnrlat=90,
    #     llcrnrlon=0,
    #     urcrnrlon=360,
    #     resolution='c')
    #
    # map.drawcoastlines()
    # map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    # map.drawmeridians(np.arange(-180, 180, 30), labels=[0, 0, 0, 1])
    #
    # x, y = map(*np.meshgrid(lon, lat))
    # clevs = np.arange(0, 371, 10)
    #
    # cnplot = map.contourf(x, y, var, clevs, cmap=plt.cm.jet)
    # cbar = map.colorbar(cnplot, location='right')

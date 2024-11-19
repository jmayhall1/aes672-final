# coding=utf-8
"""
@author: John Mark Mayhall
Last Edited: 11/19/2024
Email: jmm0111@uah.edu
"""
import datetime as dt
import glob

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from mpl_toolkits.basemap import Basemap

if __name__ == '__main__':
    plot = False
    area_flash_df = pd.DataFrame(columns=['Time', 'Count'])
    area_flash_df_event = pd.DataFrame(columns=['Time', 'Count', 'Avg'])
    # Geostationary Lightning Mapper
    for num, file in enumerate(glob.glob('C:/Users/jmayhall/Downloads/aes672_projectproposal/glm_672_data/*.nc')):
        print(f'Processing file {num + 1} of '
              f'{len(glob.glob('C:/Users/jmayhall/Downloads/aes672_projectproposal/glm_672_data/*.nc'))}')
        # G = GOES(satellite=18, product="GLM-L2-LCFA", domain='C')
        # goes_image = G.nearesttime('2024-09-26 20:00')
        newname = file.replace('C:/Users/jmayhall/Downloads/aes672_projectproposal/glm_672_data\\',
                               '').replace('.nc', '.jpg')
        if (newname[-14:-11] == '271') and (int(newname[-11: -7]) >= 500):
            continue
        if (newname[-14:-11] == '270') and (int(newname[-11: -7]) <= 2300):
            continue
        goes_image = xr.open_dataset(file)

        event_lat = goes_image.variables['event_lat'][:]
        event_lon = goes_image.variables['event_lon'][:]

        group_lat = goes_image.variables['group_lat'][:]
        group_lon = goes_image.variables['group_lon'][:]

        flash_lat = goes_image.variables['flash_lat'][:]
        flash_lon = goes_image.variables['flash_lon'][:]

        if plot:
            fig = plt.figure(figsize=(6, 6), dpi=200)
            map = Basemap(projection='merc', lat_0=30.0, lon_0=-84.0,
                          resolution='l', area_thresh=1000.0,
                          llcrnrlon=-85.0, llcrnrlat=29.0,
                          urcrnrlon=-83.0, urcrnrlat=31.0)

            map.drawcoastlines()
            map.drawcountries()
            map.fillcontinents(color='tan')
            map.drawmapboundary()

            # Plot events as large blue dots
            event_x, event_y = map(event_lon, event_lat)
            map.plot(event_x, event_y, 'bo', markersize=7)

            # Plot groups as medium green dots
            group_x, group_y = map(group_lon, group_lat)
            map.plot(group_x, group_y, 'go', markersize=3)

            # Plot flashes as small red dots
            flash_x, flash_y = map(flash_lon, flash_lat)
            map.plot(flash_x, flash_y, 'ro', markersize=1)

            plt.savefig('C:/Users/jmayhall/Downloads/aes672_projectproposal/glm_images/' +
                        file.replace('C:/Users/jmayhall/Downloads/aes672_projectproposal/glm_672_data\\',
                                     '').replace('.nc', '.jpg'))
            plt.close('all')

        flash_df = pd.DataFrame((np.array(flash_lon), np.array(flash_lat))).T
        flash_df.columns = ['Lon', 'Lat']
        count = 0
        time = (newname[-18: -5])
        no_sec = (newname[-18: -5])
        time = dt.datetime.strptime(time, '%Y%j%H%M%S')
        no_sec = dt.datetime.strptime(no_sec, '%Y%j%H%M%S')
        no_sec += dt.timedelta(minutes=5)
        no_sec -= dt.timedelta(minutes=no_sec.minute % 10,
                               seconds=no_sec.second)
        for row, column in flash_df.iterrows():
            if (-85 <= column.Lon <= -83) & (29 <= column.Lat <= 31):
                count += 1
        temp_df = pd.DataFrame([time, count, no_sec]).T
        temp_df.columns = ['Time', 'Count', 'Avg']
        area_flash_df = pd.concat((area_flash_df, temp_df))
        #
        # flash_df = pd.DataFrame((np.array(event_lon), np.array(event_lat))).T
        # flash_df.columns = ['Lon', 'Lat']
        # count = 0
        # for row, column in flash_df.iterrows():
        #     if (-85 <= column.Lon <= -83) & (29 <= column.Lat <= 31):
        #         count += 1
        # temp_df = pd.DataFrame([time, count]).T
        # temp_df.columns = ['Time', 'Count']
        # area_flash_df_event = pd.concat((area_flash_df_event, temp_df))
    # plt.plot(list(area_flash_df.Time), list(area_flash_df.Count))
    # plt.plot(list(area_flash_df_event.Time), list(area_flash_df_event.Count))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(list(area_flash_df.Time), list(area_flash_df.Count))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time (UTC)')
    plt.ylabel('Lightning Flashes')
    plt.title('Time (UTC) vs GLM Lightning Flashes for Hurricane Helene\n'
              '20 Second Count')
    plt.savefig('flashes.jpg')
    plt.show()

    avg_df = area_flash_df.groupby(['Avg'])['Count'].sum()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(list(avg_df.index), list(avg_df.values))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time (UTC)')
    plt.ylabel('Lightning Flashes')
    plt.title('Time (UTC) vs GLM Lightning Flashes for Hurricane Helene \n'
              '10 Minute Count')
    plt.savefig('flashes_avg.jpg')
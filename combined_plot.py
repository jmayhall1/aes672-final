# coding=utf-8
"""
@author: John Mark Mayhall
Last Edited: 11/19/2024
Email: jmm0111@uah.edu
"""
import datetime as dt
import glob
import os

import cartopy.crs as ccrs
import matplotlib.cm as cm
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyart
import xarray as xr
from mpl_toolkits.basemap import Basemap

if __name__ == '__main__':
    plot = True
    plotcross = True
    plotline = True
    plot_lst = []
    plot_lst30_10 = []
    plt_zdr = []
    field = 'Lightning_Class'
    level = 'lv2'
    day_lst = ['26', '27']
    variable = 'lc'
    height = 7000
    cbar_labels = ['False', 'True']
    ticks = [0, 1]
    title = 'Lightning/Graupel Identification'
    label1 = ('Graupel Classification \n'
              'Reflectivity ($Z_{e}$) dBZ, 20-60)')
    label2 = 'Graupel Classification'
    cmap_name = 'BuDRd12'
    color_map = f"pyart_{cmap_name}"
    time_lst = []
    start = (31.25, -83.5)
    end = (29.0, -84.1)
    cbar_vmin = 0
    cbar_vmax = 1

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad = os.listdir(file_dir)
        for i, file in enumerate(files_nexrad):
            if int(file[-10:-4]) > 50000 and day == '27':
                continue
            if int(file[-10:-4]) < 230000 and day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            time = dt.datetime.strptime(file[-19:-4], '%Y%m%d_%H%M%S')
            time_lst.append(time)
            radar = pyart.io.read_nexrad_archive(file_dir + file)
            kdp_maesaka = pyart.retrieve.kdp_maesaka(radar)
            radar.add_field('kdp', kdp_maesaka[0])
            radar.add_field('Lightning_Class', kdp_maesaka[0])
            grid_ktlh = pyart.map.grid_from_radars(
                radar,
                grid_shape=(30, 801, 801),
                grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                fields=['reflectivity', 'differential_reflectivity', 'cross_correlation_ratio', 'kdp',
                        'Lightning_Class'],
            )
            Zh = grid_ktlh.fields.get('reflectivity').get('data')[np.where(grid_ktlh.z.get('data') >= height)[0][0]:]
            line_data = grid_ktlh.fields.get(field).get('data')[np.where(grid_ktlh.z.get('data') == 7000)[0][0]:]
            plot_lst30_10.append((np.count_nonzero(Zh >= 30.0) / (801 * 801 * Zh.shape[0])) * 100)
            Zdr = grid_ktlh.fields.get('differential_reflectivity').get('data')[np.where(grid_ktlh.z.get('data')
                                                                                         >= height)[0][0]:]
            Zdr_0C = grid_ktlh.fields.get('differential_reflectivity').get('data')[np.where(grid_ktlh.z.get('data')
                                                                                            >= 5500)[0][0]:]
            plt_zdr.append((np.count_nonzero(Zdr_0C >= 1.0) / (801 * 801 * Zdr_0C.shape[0])) * 100)
            rho = grid_ktlh.fields.get('cross_correlation_ratio').get('data')[np.where(grid_ktlh.z.get('data')
                                                                                       >= height)[0][0]:]
            kdp = grid_ktlh.fields.get('kdp').get('data')[np.where(grid_ktlh.z.get('data') >= height)[0][0]:]
            lower = np.zeros((30 - Zh.shape[0], 801, 801))
            Zh = (Zh >= 40)
            Zdr = (Zdr >= -0.5) & (Zdr <= 3)
            rho = (rho >= 0.925)
            kdp = (kdp >= -1) & (kdp <= 2)
            final = Zh & Zdr & rho & kdp
            final = final.astype(int)
            plot_lst.append((np.count_nonzero(final == 1) / (801 * 801 * Zh.shape[0])) * 100)
            final = np.vstack([lower, final])
            grid_ktlh.fields.get('Lightning_Class')['data'] = final

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

    avg_df = area_flash_df.groupby(['Avg'])['Count'].sum()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(list(avg_df.index), list(avg_df.values), label='GLM Lightning Flashes')
    plt.plot(time_lst, np.array(plot_lst30_10) * 100, label='Pixels above 30dBZ (-10C Threshold)')
    plt.plot(time_lst, np.array(plot_lst) * 1000, label='Pixels most likely related to Lightning')
    # plt.plot(time_lst, np.array(plt_zdr) * 10, label='Pixels above 1dB (0C Threshold)')
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time (UTC)')
    plt.title('Scaled Pixels above 30dBZ with a -10C Threshold and Lightning Related Pixels\n'
              'along with Lightning Flash Count per 10 Minutes')
    plt.savefig('combined.jpg')
    plt.show()
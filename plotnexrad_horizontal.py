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

if __name__ == '__main__':
    field = 'reflectivity'
    level = 'lv2'
    day_lst = ['26', '27']
    variable = 'Zh'
    color_map = 'gist_ncar'
    label = 'Reflectivity ($Z_{h}$, dBZ)'
    time_lst = []
    # start = (30.31, -83.2)
    # end = (30.3, -84.4)
    # cbar_vmin = -10
    # cbar_vmax = 70
    # time1 = 31505
    # time2 = 315
    # start = (29.71, -83.5)
    # end = (29.7, -84.4)
    # cbar_vmin = -10
    # cbar_vmax = 70
    # time1 = 13605
    # time2 = 136
    # start = (29.51, -83.5)
    # end = (29.5, -84.4)
    # cbar_vmin = -10
    # cbar_vmax = 70
    # time1 = 10229
    # time2 = 102
    start = (29.37, -83.5)
    end = (29.36, -84.4)
    cbar_vmin = -10
    cbar_vmax = 70
    time1 = 4235
    time2 = 42
    degree = u'\N{DEGREE SIGN}'
    location_string = (f'({start[0]}{degree}N, {str(start[1])[1:]}{degree}W) to '
                       f'({end[0]}{degree}N, {str(end[1])[1:]}{degree}W)')

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad = os.listdir(file_dir)
        for i, file in enumerate(files_nexrad):
            if int(file[-10:-4]) != time1 and day == '27':
                continue
            if day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            time = dt.datetime.strptime(file[-19:-4], '%Y%m%d_%H%M%S')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Reflectivity ($Z_{h}$)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Reflectivity ($Z_{h}$)')
            radar = pyart.io.read_nexrad_archive(file_dir + file)
            grid_ktlh = pyart.map.grid_from_radars(
                radar,
                grid_shape=(30, 801, 801),
                grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                fields=[field],
            )
            fig = plt.figure(figsize=(18, 6))
            ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
            display = pyart.graph.GridMapDisplay(grid_ktlh)
            display.plot_grid(
                field,
                ax=ax1,
                title=title1,
                cmap=color_map,
                colorbar_label=label,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )

            # Plot our start and end points, as well as a line in between the two
            ax1.scatter(start[1], start[0], color="tab:blue", label="Start")
            ax1.scatter(end[1], end[0], color="black", label="End")
            ax1.plot([start[1], end[1]], [start[0], end[0]], color="k", linestyle=":")
            plt.legend(loc="upper right")

            # Add a cross-section, using our start and end points, and set our x-axis as latitude (lat)
            ax2 = plt.subplot(122)
            display.plot_cross_section(
                field,
                start,
                end,
                cmap=color_map,
                title=title2,
                colorbar_label=label,
                x_axis="lon",
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )
            plt.savefig(
                f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal-cross/{file}_{field}.jpg')
            plt.close('all')
            fig = plt.figure(figsize=(12, 4))
            display = pyart.graph.RadarMapDisplay(radar)

            ax = plt.subplot(111, projection=ccrs.PlateCarree())

            display.plot_ppi_map(
                field,
                ax=ax,
                cmap=color_map,
                title=title1,
                colorbar_label=label,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
                min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
            )
            plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal/{file}_{field}.jpg')
            plt.close('all')

    field = 'differential_reflectivity'
    level = 'lv2'
    day_lst = ['26', '27']
    variable = 'Zdr'
    label1 = 'Differential Reflectivity ($Z_{dr}$)'
    label2 = ('Reflectivity ($Z_{h}$, dBZ)\n'
              'Differential Reflectivity ($Z_{dr}$, dB)')
    color_map = 'gist_ncar'
    cbar_vmin = -2
    cbar_vmax = 2

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad = os.listdir(file_dir)
        for i, file in enumerate(files_nexrad):
            if int(file[-10:-4]) != time1 and day == '27':
                continue
            if day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            radar = pyart.io.read_nexrad_archive(file_dir + file)
            time = dt.datetime.strptime(file[-19:-4], '%Y%m%d_%H%M%S')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Differential Reflectivity ($Z_{dr}$)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Differential Reflectivity ($Z_{dr}$) & Reflectivity ($Z_{h}$)')
            grid_ktlh = pyart.map.grid_from_radars(
                radar,
                grid_shape=(30, 801, 801),
                grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                fields=[field, 'reflectivity'],
            )
            # Setup the figure, and plot our x/y view of the radar
            fig = plt.figure(figsize=(18, 6))
            ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
            display = pyart.graph.GridMapDisplay(grid_ktlh)
            display.plot_grid(
                field,
                ax=ax1,
                title=title1,
                cmap=color_map,
                colorbar_label=label1,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )

            # Plot our start and end points, as well as a line in between the two
            ax1.scatter(start[1], start[0], color="navy", label="Start")
            ax1.scatter(end[1], end[0], color="black", label="End")
            ax1.plot([start[1], end[1]], [start[0], end[0]], color="k", linestyle=":")
            plt.legend(loc="upper right")

            # Add a cross-section, using our start and end points, and set our x-axis as latitude (lat)
            ax2 = plt.subplot(122)
            display.plot_cross_section(
                field,
                start,
                end,
                title='',
                cmap=color_map,
                colorbar_label=label2,
                x_axis="lon",
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )
            display.plot_cross_section(
                'reflectivity',
                start,
                end,
                alpha=0.4,
                title=title2,
                cmap='gray',
                colorbar_label='',
                x_axis="lon",
                vmin=0,
                vmax=50,
            )
            plt.savefig(
                f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal-cross/{file}_{field}.jpg')
            plt.close('all')
            fig = plt.figure(figsize=(12, 4))
            display = pyart.graph.RadarMapDisplay(radar)

            ax = plt.subplot(111, projection=ccrs.PlateCarree())

            display.plot_ppi_map(
                field,
                ax=ax,
                title=title1,
                cmap=color_map,
                colorbar_label=label1,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
                min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
            )
            plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal/{file}_{field}.jpg')
            plt.close('all')

    field = 'cross_correlation_ratio'
    level = 'lv2'
    day_lst = ['26', '27']
    variable = 'rho'
    label1 = 'Correlation Coefficient ($ρ_{hv}$)'
    label2 = ('Reflectivity ($Z_{h}$, dBZ)\n'
              'Correlation Coefficient ($ρ_{hv}$)')
    color_map = 'rainbow'
    cbar_vmin = 0.8
    cbar_vmax = 1

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad = os.listdir(file_dir)
        for i, file in enumerate(files_nexrad):
            if int(file[-10:-4]) != time1 and day == '27':
                continue
            if day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            time = dt.datetime.strptime(file[-19:-4], '%Y%m%d_%H%M%S')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Correlation Coefficient ($ρ_{hv}$)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Correlation Coefficient ($ρ_{hv}$) & Reflectivity ($Z_{h}$)')
            radar = pyart.io.read_nexrad_archive(file_dir + file)
            grid_ktlh = pyart.map.grid_from_radars(
                radar,
                grid_shape=(30, 801, 801),
                grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                fields=[field, 'reflectivity'],
            )

            # Setup the figure, and plot our x/y view of the radar
            fig = plt.figure(figsize=(20, 6))
            ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
            display = pyart.graph.GridMapDisplay(grid_ktlh)
            display.plot_grid(
                field,
                ax=ax1,
                cmap=color_map,
                title=title1,
                colorbar_label=label1,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )

            # Plot our start and end points, as well as a line in between the two
            ax1.scatter(start[1], start[0], color="tab:blue", label="Start")
            ax1.scatter(end[1], end[0], color="black", label="End")
            ax1.plot([start[1], end[1]], [start[0], end[0]], color="k", linestyle=":")
            plt.legend(loc="upper right")

            # Add a cross-section, using our start and end points, and set our x-axis as latitude (lat)
            ax2 = plt.subplot(122)
            display.plot_cross_section(
                field,
                start,
                end,
                cmap=color_map,
                title='',
                colorbar_label=label2,
                x_axis="lon",
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )
            display.plot_cross_section(
                'reflectivity',
                start,
                end,
                title=title2,
                alpha=0.4,
                cmap='gray',
                colorbar_label='',
                x_axis="lon",
                vmin=0,
                vmax=50,
            )
            plt.savefig(
                f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal-cross/{file}_{field}.jpg')
            plt.close('all')
            fig = plt.figure(figsize=(12, 4))
            display = pyart.graph.RadarMapDisplay(radar)

            ax = plt.subplot(111, projection=ccrs.PlateCarree())

            display.plot_ppi_map(
                field,
                ax=ax,
                title=title1,
                cmap=color_map,
                colorbar_label=label1,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
                min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
            )
            plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal/{file}_{field}.jpg')
            plt.close('all')

    field = 'specific_differential_phase'
    level = 'lv3'
    day_lst = ['27']
    # Note that NU is for not used and is there as a placeholder.
    variable = 'Kdp'
    label1 = 'Specific Differential Phase ($K_{dp}$)'
    label2 = ('Reflectivity ($Z_{h}$, dBZ)\n'
              'Specific Differential Phase ($K_{dp}$)')
    color_map = 'gist_ncar'
    vmin = -2
    vmax = 6

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad_all = os.listdir(file_dir)
        files_nexrad_allscans = [file for file in files_nexrad_all if
                                 ('N0K' in file) or ('N1K' in file) or ('NAK' in file)
                                 or ('NBK' in file) or ('N2K' in file) or ('N3K' in file)]
        files_nexrad = [file for file in files_nexrad_all if ('N0K' in file)]
        for i, file in enumerate(files_nexrad):
            if int(file[-4:]) != time2 and day == '27':
                continue
            if day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            radar = pyart.io.read_nexrad_level3(file_dir + file)
            time = dt.datetime.strptime(file[-12:], '%Y%m%d%H%M')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Specific Differential Phase ($K_{dp}$)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Specific Differential Phase ($K_{dp}$) & Reflectivity ($Z_{h}$)')
            nexrad_file_lst = glob.glob(f'C:/Users/jmayhall/Downloads/'
                                        f'aes672_projectproposal/ktlh_data/lv2'
                                        f'-sept{day}/*')
            try:
                nexrad_file = [nex for nex in nexrad_file_lst if f'KTLH{file[-12: -4]}_{file[-4:]}' in nex][0]
                radar_nex = pyart.io.read_nexrad_archive(nexrad_file)
                radarA = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('NAK' in fileA) and (file[-12:] in fileA)][0])
                radar1 = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('N1K' in fileA) and (file[-12:] in fileA)][0])
                radarB = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('NBK' in fileA) and (file[-12:] in fileA)][0])
                radar2 = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('N2K' in fileA) and (file[-12:] in fileA)][0])
                radar3 = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('N3K' in fileA) and (file[-12:] in fileA)][0])

                grid_ktlh = pyart.map.grid_from_radars(
                    [radar, radarA, radar1, radarB, radar2, radar3],
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=[field],
                )
                grid_ktlh_nex = pyart.map.grid_from_radars(
                    [radar_nex],
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=['reflectivity'],
                )

                # Setup the figure, and plot our x/y view of the radar
                fig = plt.figure(figsize=(18, 6))
                ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
                display = pyart.graph.GridMapDisplay(grid_ktlh)
                display_nex = pyart.graph.GridMapDisplay(grid_ktlh_nex)
                display.plot_grid(
                    field,
                    ax=ax1,
                    cmap=color_map,
                    colorbar_label=label1,
                    title=title1,
                    vmin=vmin,
                    vmax=vmax,
                )

                # Plot our start and end points, as well as a line in between the two
                ax1.scatter(start[1], start[0], color="tab:blue", label="Start")
                ax1.scatter(end[1], end[0], color="black", label="End")
                ax1.plot([start[1], end[1]], [start[0], end[0]], color="k", linestyle=":")
                plt.legend(loc="upper right")

                # Add a cross-section, using our start and end points, and set our x-axis as latitude (lat)
                ax2 = plt.subplot(122)
                display.plot_cross_section(
                    field,
                    start,
                    end,
                    cmap=color_map,
                    vmin=vmin,
                    vmax=vmax,
                    colorbar_label=label2,
                    title='',
                    x_axis="lon",
                )
                display_nex.plot_cross_section(
                    'reflectivity',
                    start,
                    end,
                    alpha=0.5,
                    cmap='gray',
                    colorbar_label='',
                    x_axis="lon",
                    title=title2,
                    vmin=0,
                    vmax=50,
                )
                plt.savefig(
                    f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal-cross/{file}_{field}.jpg')
                plt.close('all')
            except IndexError:
                continue
            fig = plt.figure(figsize=(12, 4))
            display = pyart.graph.RadarMapDisplay(radar)

            ax = plt.subplot(111, projection=ccrs.PlateCarree())

            display.plot_ppi_map(
                field,
                ax=ax,
                cmap=color_map,
                vmin=vmin,
                vmax=vmax,
                colorbar_label=label1,
                title=title1,
                min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
            )
            plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal/{file}_{field}.jpg')
            plt.close('all')

    field = 'radar_echo_classification'
    level = 'lv3'
    day_lst = ['27']
    cbar_labels = ['ND', 'BI', 'GC', 'IC', 'DS', 'WS', 'RA', 'HR', 'BD', 'GR', 'HA', 'LH', 'GH', 'NU', 'UK', 'RH']
    ticks = np.linspace(0, 150, len(cbar_labels))
    # Note that NU is for not used and is there as a placeholder.
    variable = 'hydro'
    label1 = 'Hydrometeor Identification (HID)'
    label2 = ('Reflectivity ($Z_{h}$, dBZ)\n'
              'Hydrometeor Identification (HID)')
    cmap_name = "ChaseSpectral"
    color_map = f"pyart_{cmap_name}"
    vmin = 0
    vmax = 150

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad_all = os.listdir(file_dir)
        files_nexrad_allscans = [file for file in files_nexrad_all if
                                 ('N0H' in file) or ('N1H' in file) or ('NAH' in file)
                                 or ('NBH' in file) or ('N2H' in file) or ('N3H' in file)]
        files_nexrad = [file for file in files_nexrad_all if ('N0H' in file)]
        for i, file in enumerate(files_nexrad):
            if int(file[-4:]) != time2 and day == '27':
                continue
            if day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            time = dt.datetime.strptime(file[-12:], '%Y%m%d%H%M')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Hydrometeor Identification (HID)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Hydrometeor Identification (HID) & Reflectivity ($Z_{h}$)')
            radar = pyart.io.read_nexrad_level3(file_dir + file)
            nexrad_file_lst = glob.glob(f'C:/Users/jmayhall/Downloads/'
                                        f'aes672_projectproposal/ktlh_data/lv2'
                                        f'-sept{day}/*')
            try:
                nexrad_file = [nex for nex in nexrad_file_lst if f'KTLH{file[-12: -4]}_{file[-4:]}' in nex][0]
                radar_nex = pyart.io.read_nexrad_archive(nexrad_file)
                radarA = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('NAH' in fileA) and (file[-12:] in fileA)][0])
                radar1 = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('N1H' in fileA) and (file[-12:] in fileA)][0])
                radarB = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('NBH' in fileA) and (file[-12:] in fileA)][0])
                radar2 = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('N2H' in fileA) and (file[-12:] in fileA)][0])
                radar3 = pyart.io.read_nexrad_level3(file_dir + [fileA for fileA in files_nexrad_allscans
                                                                 if ('N3H' in fileA) and (file[-12:] in fileA)][0])

                grid_ktlh = pyart.map.grid_from_radars(
                    [radar, radarA, radar1, radarB, radar2, radar3],
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=[field],
                )
                grid_ktlh_nex = pyart.map.grid_from_radars(
                    [radar_nex],
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=['reflectivity'],
                )
                grid_ktlh.fields[field]['data'] = np.round(grid_ktlh.fields.get(field).get('data'), -1)

                # Setup the figure, and plot our x/y view of the radar
                fig = plt.figure(figsize=(18, 6))
                ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
                display = pyart.graph.GridMapDisplay(grid_ktlh)
                display_nex = pyart.graph.GridMapDisplay(grid_ktlh_nex)
                display.plot_grid(
                    field,
                    ax=ax1,
                    cmap=cm.get_cmap(color_map, 16),
                    ticks=ticks,
                    ticklabs=cbar_labels,
                    colorbar_label=label1,
                    title=title1,
                    vmin=vmin,
                    vmax=vmax,
                )

                # Plot our start and end points, as well as a line in between the two
                ax1.scatter(start[1], start[0], color="tab:blue", label="Start")
                ax1.scatter(end[1], end[0], color="black", label="End")
                ax1.plot([start[1], end[1]], [start[0], end[0]], color="k", linestyle=":")
                plt.legend(loc="upper right")

                # Add a cross-section, using our start and end points, and set our x-axis as latitude (lat)
                ax2 = plt.subplot(122)
                display.plot_cross_section(
                    field,
                    start,
                    end,
                    cmap=cm.get_cmap(color_map, 16),
                    ticks=ticks,
                    ticklabs=cbar_labels,
                    vmin=vmin,
                    vmax=vmax,
                    colorbar_label=label2,
                    title='',
                    x_axis="lon",
                )
                display_nex.plot_cross_section(
                    'reflectivity',
                    start,
                    end,
                    alpha=0.5,
                    cmap='gray',
                    colorbar_label='',
                    x_axis="lon",
                    title=title2,
                    vmin=0,
                    vmax=50,
                )
                plt.savefig(
                    f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal-cross/{file}_{field}.jpg')
                plt.close('all')
            except IndexError:
                continue
            fig = plt.figure(figsize=(12, 4))
            display = pyart.graph.RadarMapDisplay(radar)

            ax = plt.subplot(111, projection=ccrs.PlateCarree())

            display.plot_ppi_map(
                field,
                ax=ax,
                cmap=cm.get_cmap(color_map, 16),
                ticks=ticks,
                ticklabs=cbar_labels,
                vmin=vmin,
                vmax=vmax,
                colorbar_label=label1,
                title=title1,
                min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
            )
            plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal/{file}_{field}.jpg')
            plt.close('all')

    field = 'Lightning_Class'
    level = 'lv2'
    day_lst = ['26', '27']
    variable = 'lc'
    height = 7000
    cbar_labels = ['False', 'True']
    ticks = [0, 1]
    label1 = 'Graupel Classification'
    label2 = ('Reflectivity ($Z_{h}$, dBZ)\n'
              f'Graupel Classification')
    cmap_name = 'BuDRd12'
    color_map = f"pyart_{cmap_name}"
    cbar_vmin = 0
    cbar_vmax = 1

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad = os.listdir(file_dir)
        for i, file in enumerate(files_nexrad):
            if int(file[-10:-4]) != time1 and day == '27':
                continue
            if day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            time = dt.datetime.strptime(file[-19:-4], '%Y%m%d_%H%M%S')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Graupel Classification')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Graupel Classification & Reflectivity ($Z_{h}$)')
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
            Zdr = grid_ktlh.fields.get('differential_reflectivity').get('data')[
                  np.where(grid_ktlh.z.get('data') >= height)[0][0]:]
            rho = grid_ktlh.fields.get('cross_correlation_ratio').get('data')[
                  np.where(grid_ktlh.z.get('data') >= height)[0][0]:]
            kdp = grid_ktlh.fields.get('kdp').get('data')[np.where(grid_ktlh.z.get('data') >= height)[0][0]:]
            lower = np.zeros((30 - Zh.shape[0], 801, 801))
            Zh = (Zh >= 40)
            Zdr = (Zdr >= -0.5) & (Zdr <= 3)
            rho = (rho >= 0.925)
            kdp = (kdp >= -1) & (kdp <= 2)
            final = Zh & Zdr & rho & kdp
            final = final.astype(int)
            final = np.vstack([lower, final])
            print(np.unique(final))
            grid_ktlh.fields.get('Lightning_Class')['data'] = final
            # Setup the figure, and plot our x/y view of the radar
            fig = plt.figure(figsize=(18, 6))
            ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
            display = pyart.graph.GridMapDisplay(grid_ktlh)
            display.plot_grid(
                field,
                ax=ax1,
                cmap=cm.get_cmap(color_map, 2),
                ticks=ticks,
                ticklabs=cbar_labels,
                colorbar_label=label1,
                title=title1,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )

            # Plot our start and end points, as well as a line in between the two
            ax1.scatter(start[1], start[0], color="tab:orange", label="Start")
            ax1.scatter(end[1], end[0], color="white", label="End")
            ax1.plot([start[1], end[1]], [start[0], end[0]], color="w", linestyle=":")
            plt.legend(loc="upper right")

            # Add a cross-section, using our start and end points, and set our x-axis as latitude (lat)
            ax2 = plt.subplot(122)
            display.plot_cross_section(
                field,
                start,
                end,
                title='',
                cmap=cm.get_cmap(color_map, 2),
                ticks=ticks,
                ticklabs=cbar_labels,
                colorbar_label=label2,
                x_axis="lon",
                vmin=cbar_vmin,
                vmax=cbar_vmax,
            )
            display.plot_cross_section(
                'reflectivity',
                start,
                end,
                alpha=0.4,
                title=title2,
                cmap='gray',
                colorbar_label='',
                x_axis="lon",
                vmin=0,
                vmax=50,
            )
            plt.savefig(
                f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal-cross/{file}_{field}.jpg')
            plt.close('all')
            fig = plt.figure(figsize=(12, 4))
            display = pyart.graph.RadarMapDisplay(radar)

            ax = plt.subplot(111, projection=ccrs.PlateCarree())

            display.plot_ppi_map(
                field,
                ax=ax,
                title=title1,
                cmap=cm.get_cmap(color_map, 2),
                ticks=ticks,
                ticklabs=cbar_labels,
                colorbar_label=label1,
                vmin=cbar_vmin,
                vmax=cbar_vmax,
                min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
            )
            plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/horizontal/{file}_{field}.jpg')
            plt.close('all')

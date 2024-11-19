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
    plot = True
    plotcross = True
    plotline = True
    plot_lst30, plot_lst40, plot_lst50 = [], [], []
    plot_lst30_10, plot_lst40_10, plot_lst50_10 = [], [], []
    field = 'specific_differential_phase'
    level = 'lv3'
    day_lst = ['27']
    # Note that NU is for not used and is there as a placeholder.
    variable = 'Kdp'
    label1 = 'Specific Differential Phase ($K_{dp}$)'
    label2 = ('Reflectivity ($Z_{h}$, dBZ)\n'
              'Specific Differential Phase ($K_{dp}$)')
    color_map = 'gist_ncar'

    time_lst = []
    vmin = -2
    vmax = 6
    start = (31.25, -83.5)
    end = (29.0, -84.1)
    degree = u'\N{DEGREE SIGN}'
    location_string = (f'({start[0]}{degree}N, {str(start[1])[1:]}{degree}W) to '
                       f'({end[0]}{degree}N, {str(end[1])[1:]}{degree}W)')

    for day in day_lst:
        file_dir = f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}/'
        files_nexrad_all = os.listdir(file_dir)
        files_nexrad_allscans = [file for file in files_nexrad_all if
                                 ('N0K' in file) or ('N1K' in file) or ('NAK' in file)
                                 or ('NBK' in file) or ('N2K' in file) or ('N3K' in file)]
        files_nexrad = [file for file in files_nexrad_all if ('N0K' in file)]
        for i, file in enumerate(files_nexrad):
            if int(file[-4:]) > 500 and day == '27':
                continue
            if int(file[-4:]) < 2300 and day == '26':
                continue
            print(f'Processing file {i + 1} of {len(files_nexrad)}')
            time = dt.datetime.strptime(file[-12:], '%Y%m%d%H%M')
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Specific Differential Phase ($K_{dp}$)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Specific Differential Phase ($K_{dp}$) & Reflectivity ($Z_{h}$)')
            radar = pyart.io.read_nexrad_level3(file_dir + file)
            if plotcross:
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
                    time_lst.append(time)
                    line_data = grid_ktlh.fields.get(field).get('data')[
                                np.where(grid_ktlh.z.get('data') == 5500)[0][0]:]
                    plot_lst30.append((np.count_nonzero(line_data > 0) / (801 * 801 * line_data.shape[0])) * 100)
                    plot_lst40.append((np.count_nonzero(line_data < 0) / (801 * 801 * line_data.shape[0])) * 100)
                    plot_lst50.append((np.count_nonzero(line_data == 0) / (801 * 801 * line_data.shape[0])) * 100)

                    line_data = grid_ktlh.fields.get(field).get('data')[
                                np.where(grid_ktlh.z.get('data') == 7000)[0][0]:]
                    plot_lst30_10.append((np.count_nonzero(line_data > 0) / (801 * 801 * line_data.shape[0])) * 100)
                    plot_lst40_10.append((np.count_nonzero(line_data < 0) / (801 * 801 * line_data.shape[0])) * 100)
                    plot_lst50_10.append((np.count_nonzero(line_data == 0) / (801 * 801 * line_data.shape[0])) * 100)

                    # Setup the figure, and plot our x/y view of the radar
                    fig = plt.figure(figsize=(18, 6))
                    ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
                    display = pyart.graph.GridMapDisplay(grid_ktlh)
                    display_nex = pyart.graph.GridMapDisplay(grid_ktlh_nex)
                    display.plot_grid(
                        field,
                        ax=ax1,
                        cmap=color_map,
                        title=title1,
                        colorbar_label=label1,
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
                        title='',
                        vmin=vmin,
                        vmax=vmax,
                        colorbar_label=label2,
                        x_axis="lat",
                    )
                    display_nex.plot_cross_section(
                        'reflectivity',
                        start,
                        end,
                        alpha=0.5,
                        cmap='gray',
                        title=title2,
                        colorbar_label='',
                        x_axis="lat",
                        vmin=0,
                        vmax=50,
                    )
                    plt.savefig(
                        f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/'
                        f'{level}-sept{day}-{variable}images-cross/{file}.jpg')
                    plt.close('all')
                except IndexError:
                    print(f'Skipping: {time}')
                    continue
            if plot:
                fig = plt.figure(figsize=(12, 4))
                display = pyart.graph.RadarMapDisplay(radar)

                ax = plt.subplot(111, projection=ccrs.PlateCarree())

                display.plot_ppi_map(
                    field,
                    ax=ax,
                    cmap=color_map,
                    title=title1,
                    vmin=vmin,
                    vmax=vmax,
                    colorbar_label=label1,
                    min_lat=29.0, max_lat=31.0, min_lon=-85.0, max_lon=-83.0,
                )
                plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}-'
                            f'{variable}images/{file}.jpg')
                plt.close('all')

    if plotline:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator())
        plt.plot(time_lst, plot_lst30, label=r'$K_{dp} > 0$')
        plt.plot(time_lst, plot_lst40, label=r'$K_{dp} < 0$')
        plt.plot(time_lst, plot_lst50, label=r'$K_{dp} = 0$')
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time (UTC)')
        plt.ylabel('Percent (%) of $K_{dp}$ Pixels based on Threshold (0C)')
        plt.title('Time vs Cross-Pixel Percentage of $K_{dp}$ Pixels based on Threshold (0C)')
        plt.show()

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator())
        plt.plot(time_lst, plot_lst30_10, label=r'$K_{dp} > 0$')
        plt.plot(time_lst, plot_lst40_10, label=r'$K_{dp} < 0$')
        plt.plot(time_lst, plot_lst50_10, label=r'$K_{dp} = 0$')
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time (UTC)')
        plt.ylabel('Percent (%) of $K_{dp}$ Pixels based on Threshold (-10C)')
        plt.title('Time vs Cross-Pixel Percentage of $K_{dp}$ Pixels based on Threshold (-10C)')
        plt.show()
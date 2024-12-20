# coding=utf-8
"""
@author: John Mark Mayhall
Last Edited: 11/19/2024
Email: jmm0111@uah.edu
"""
import datetime as dt
import os

import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pyart

if __name__ == '__main__':
    plot = True
    plotcross = True
    plotline = True
    plot_lst30, plot_lst40 = [], []
    plot_lst30_10, plot_lst40_10 = [], []
    field = 'reflectivity'
    level = 'lv2'
    day_lst = ['26', '27']
    variable = 'Zh'
    label = 'Reflectivity ($Z_{h}$, dBZ)'
    color_map = 'gist_ncar'
    time_lst = []
    start = (31.25, -83.5)
    end = (29.0, -84.1)
    degree = u'\N{DEGREE SIGN}'
    location_string = (f'({start[0]}{degree}N, {str(start[1])[1:]}{degree}W) to '
                       f'({end[0]}{degree}N, {str(end[1])[1:]}{degree}W)')
    cbar_vmin = -10
    cbar_vmax = 70

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
            time_string = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%SZ')
            title1 = (f'{time_string}\n'
                      'Reflectivity ($Z_{h}$)')
            title2 = (f'{location_string}\n'
                      f'{time_string}\n'
                      'Reflectivity ($Z_{h}$)')
            radar = pyart.io.read_nexrad_archive(file_dir + file)
            if not plotcross and plotline:
                grid_ktlh = pyart.map.grid_from_radars(
                    radar,
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=[field],
                )
                line_data = grid_ktlh.fields.get(field).get('data')[np.where(grid_ktlh.z.get('data') == 5500)[0][0]:]
                plot_lst30.append((np.count_nonzero(line_data >= 30.0) / (801 * 801 * line_data.shape[0])) * 100)
                plot_lst40.append((np.count_nonzero(line_data >= 40.0) / (801 * 801 * line_data.shape[0])) * 100)

                line_data = grid_ktlh.fields.get(field).get('data')[np.where(grid_ktlh.z.get('data') == 7000)[0][0]:]
                plot_lst30_10.append((np.count_nonzero(line_data >= 30.0) / (801 * 801 * line_data.shape[0])) * 100)
                plot_lst40_10.append((np.count_nonzero(line_data >= 40.0) / (801 * 801 * line_data.shape[0])) * 100)
            if plotcross:
                grid_ktlh = pyart.map.grid_from_radars(
                    radar,
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=[field],
                )
                line_data = grid_ktlh.fields.get(field).get('data')[np.where(grid_ktlh.z.get('data') == 5500)[0][0]:]
                plot_lst30.append((np.count_nonzero(line_data >= 30.0) / (801 * 801 * line_data.shape[0])) * 100)
                plot_lst40.append((np.count_nonzero(line_data >= 40.0) / (801 * 801 * line_data.shape[0])) * 100)

                line_data = grid_ktlh.fields.get(field).get('data')[np.where(grid_ktlh.z.get('data') == 7000)[0][0]:]
                plot_lst30_10.append((np.count_nonzero(line_data >= 30.0) / (801 * 801 * line_data.shape[0])) * 100)
                plot_lst40_10.append((np.count_nonzero(line_data >= 40.0) / (801 * 801 * line_data.shape[0])) * 100)
                # Setup the figure, and plot our x/y view of the radar
                fig = plt.figure(figsize=(18, 6))
                ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
                display = pyart.graph.GridMapDisplay(grid_ktlh)
                display.plot_grid(
                    field,
                    ax=ax1,
                    cmap=color_map,
                    title=title1,
                    colorbar_label=label,
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
                    cmap=color_map,
                    title=title2,
                    colorbar_label=label,
                    x_axis="lat",
                    vmin=cbar_vmin,
                    vmax=cbar_vmax,
                )
                plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}-'
                            f'{variable}images-cross/{file}.jpg')
                plt.close('all')
            if plot:
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
                plt.savefig(f'C:/Users/jmayhall/Downloads/aes672_projectproposal/ktlh_data/{level}-sept{day}-'
                            f'{variable}images/{file}.jpg')
                plt.close('all')

    if plotline:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator())
        plt.plot(time_lst, plot_lst30, label='Pixels above 30dBZ')
        plt.plot(time_lst, plot_lst40, label='Pixels above 40dBz')
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time (UTC)')
        plt.ylabel('Percent (%) of Pixels above $Z_{h}$ Threshold (0C)')
        plt.title('Time vs Cross-Pixel Percentage above $Z_{h}$ Threshold (0C)')
        plt.show()

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator())
        plt.plot(time_lst, plot_lst30_10, label='Pixels above 30dBZ')
        plt.plot(time_lst, plot_lst40_10, label='Pixels above 40dBz')
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time (UTC)')
        plt.ylabel('Percent (%) of Pixels above $Z_{h}$ Threshold (-10C)')
        plt.title('Time vs Cross-Pixel Percentage above $Z_{h}$ Threshold (-10C)')
        plt.show()
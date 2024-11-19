# coding=utf-8
"""
@author: John Mark Mayhall
Last Edited: 11/19/2024
Email: jmm0111@uah.edu
"""
import datetime as dt
import os

import cartopy.crs as ccrs
import matplotlib.cm as cm
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pyart

if __name__ == '__main__':
    plot = True
    plotcross = True
    plotline = True
    plot_lst = []
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
    time_lst = []
    start = (31.25, -83.5)
    end = (29.0, -84.1)
    degree = u'\N{DEGREE SIGN}'
    location_string = (f'({start[0]}{degree}N, {str(start[1])[1:]}{degree}W) to '
                       f'({end[0]}{degree}N, {str(end[1])[1:]}{degree}W)')
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
            if not plotcross and plotline:
                grid_ktlh = pyart.map.grid_from_radars(
                    radar,
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=['reflectivity', 'differential_reflectivity', 'cross_correlation_ratio', 'kdp'],
                )
                Zh = grid_ktlh.fields.get('reflectivity').get('data')[np.where(grid_ktlh.z.get('data')
                                                                               >= height)[0][0]:]
                Zdr = grid_ktlh.fields.get('differential_reflectivity').get('data')[np.where(grid_ktlh.z.get('data')
                                                                                             >= height)[0][0]:]
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
                final = np.vstack([lower, final])
                grid_ktlh.fields.get('Lightning_Class')['data'] = final

                plot_lst.append((np.count_nonzero(final == 1) / (801 * 801 * final.shape[0])) * 100)
            if plotcross:
                grid_ktlh = pyart.map.grid_from_radars(
                    radar,
                    grid_shape=(30, 801, 801),
                    grid_limits=((500, 15000), (-200000, 200000), (-200000, 200000)),
                    grid_origin=(radar.latitude['data'][0], radar.longitude['data'][0]),
                    fields=['reflectivity', 'differential_reflectivity', 'cross_correlation_ratio', 'kdp',
                            'Lightning_Class'],
                )
                Zh = grid_ktlh.fields.get('reflectivity').get('data')[np.where(grid_ktlh.z.get('data')
                                                                               >= height)[0][0]:]
                Zdr = grid_ktlh.fields.get('differential_reflectivity').get('data')[np.where(grid_ktlh.z.get('data')
                                                                                             >= height)[0][0]:]
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
                # Setup the figure, and plot our x/y view of the radar
                fig = plt.figure(figsize=(18, 6))
                ax1 = plt.subplot(121, projection=ccrs.PlateCarree())
                display = pyart.graph.GridMapDisplay(grid_ktlh)
                display.plot_grid(
                    field,
                    ax=ax1,
                    title=title1,
                    cmap=cm.get_cmap(color_map, 2),
                    ticks=ticks,
                    ticklabs=cbar_labels,
                    colorbar_label=label1,
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
                    x_axis="lat",
                    vmin=cbar_vmin,
                    vmax=cbar_vmax,
                )
                display.plot_cross_section(
                    'reflectivity',
                    start,
                    end,
                    alpha=0.4,
                    cmap='gray',
                    title=title2,
                    colorbar_label='',
                    x_axis="lat",
                    vmin=0,
                    vmax=50,
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
                    title=title1,
                    cmap=cm.get_cmap(color_map, 2),
                    ticks=ticks,
                    ticklabs=cbar_labels,
                    colorbar_label=label1,
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
        plt.plot(time_lst, plot_lst, label='Pixels most likely related to Lightning')
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time (UTC)')
        plt.ylabel(r'Percent (%) of Pixels related to Lightning')
        plt.title(r'Time vs Cross-Pixel Percentage related to Lightning')
        plt.show()
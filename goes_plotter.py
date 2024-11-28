# coding=utf-8
from goes2go import GOES
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

degree_sign = u'\N{DEGREE SIGN}'
G = GOES(satellite=16, product="ABI-L2-MCMIPC", domain='M').nearesttime('2024-09-26 21:00')

ax = plt.subplot(projection=G.rgb.crs)
ax.imshow(G.rgb.TrueColor(), **G.rgb.imshow_kwargs, )
ax.coastlines()
ax.set_title('GOES-16 True Color Mesoscale Sector Image\n'
             '2024-09-26 21:00')
plt.show()

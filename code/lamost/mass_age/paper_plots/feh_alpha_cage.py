import pyfits
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import cm
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
import numpy as np

direc = "/Users/annaho/Data/LAMOST/Mass_And_Age"
hdulist = pyfits.open("%s/lamost_catalog_mass_age_with_cuts.fits" %direc)
tbdata = hdulist[1].data
hdulist.close()
mh = tbdata.field("cannon_mh")
afe = tbdata.field("cannon_afe")
age = tbdata.field("cannon_age")
snr = tbdata.field("cannon_snrg")
teff = tbdata.field("cannon_teff")
logg = tbdata.field("cannon_logg")
cm = tbdata.field("cannon_cm")
nm = tbdata.field("cannon_nm")
chisq = tbdata.field("chisq")

mh = tbdata.field("apogee_mh")
afe = tbdata.field("apogee_afe")
age = tbdata.field("cannon_age")
snr = tbdata.field("cannon_snrg")
teff = tbdata.field("apogee_teff")
logg = tbdata.field("apogee_logg") 
cm = tbdata.field("apogee_cm")
nm = tbdata.field("apogee_nm")

#cannon = np.vstack((cannon_mh, cannon_afe, cannon_age)).T

low = min(mh)
high = max(mh)

low2 = -0.1
high2 = 0.35

tr_choose = tbdata.field("is_ref_obj").astype(bool)
mh = tbdata.field("apogee_mh")
afe = tbdata.field("apogee_afe")

afe_choose = np.logical_and(afe > -0.03, afe < 0.3)
more_cuts = np.logical_and(mh < 0.25, afe_choose)
snr_choose = np.logical_and(snr > 100, snr < 200)
chisq_choose = np.logical_and(chisq > 300, chisq < 4000)
choose_quality = np.logical_and(snr_choose, chisq_choose)
choose = tr_choose
#choose = np.logical_and(choose_quality, more_cuts)

hist1,x2,y2,temp = plt.hist2d(
        mh[choose], afe[choose], weights=age[choose], bins=30, cmin = 5)
hist1_norm,x3,y3,temp = plt.hist2d(
        mh[choose], afe[choose], bins=30, cmin = 5)
image = np.array(hist1)/np.array(hist1_norm)
#image = hist1
image = np.array(image)
print(image)
bad = np.where(np.isnan(image))
image[bad] = None
print(image)
im = plt.imshow(
        image.T, interpolation="nearest" ,aspect = 'auto',
        origin = 'lower', cmap=plt.cm.RdYlBu_r,
        vmin=0, vmax=12,
        #norm=LogNorm(vmin=1, vmax=12),
        extent = (x3.min(), x3.max(), y3.min(), y3.max() ),alpha=0.8)
plt.colorbar(im, label="Median Age [Gyr]", ticks=[1,4,7,10], format='$%.2f$')
plt.show()
 

def plot_subplots():
    fig,axarr = plt.subplots(1,3, figsize=(15,5.5), sharex=True, sharey=True)

    names = [r'SNR \textgreater 100', r'100 \textgreater SNR \textgreater 60', 
    r'60 \textgreater SNR \textgreater 30']
    snr_min = [100, 60, 30]

    for i in range(0, len(names)):
        ax = axarr[i]
        if i == 0:
            choose = snr > 100
        elif i == 1:
            choose = np.logical_and(snr > 60, snr < 100)
        elif i == 2:
            choose = np.logical_and(snr < 60, snr > 30)
        hist1,x2,y2,temp = plt.hist2d(
                mh[choose], afe[choose], weights=age[choose], bins=30,cmin = 10)
        hist1_norm,x3,y3,temp = plt.hist2d(
                mh[choose], afe[choose], bins=30,cmin = 10)
        image = hist1/hist1_norm
        #bad = np.isnan(image)
        #image[bad] = None
        im = ax.imshow(
                image.T, interpolation="nearest" ,aspect = 'auto',
                origin = 'lower', cmap=plt.cm.RdYlBu_r,vmin=0, vmax=12,
                extent = (x3.min(), x3.max(), y3.min(), y3.max() ),alpha=0.8)
        ax.set_axis_bgcolor('#D0D0D0')
        # im = ax.scatter(
        #         mh[choose],afe[choose],c=age[choose], 
        #         s=1, lw=0, cmap=cmap, vmin=1, vmax=12,
        #         norm=LogNorm())
        ax.set_xlabel(r"$\mbox{[Fe/H] (K)}$", fontsize=16)
        if i == 0:
            ax.set_ylabel(r"$\mbox{[$\alpha$/Fe] (dex)}$", fontsize=16)
        ax.set_title("%s" %names[i], fontsize=16)
        ax.set_xlim(low,high)
        ax.set_ylim(low2,high2)
        ax.tick_params(axis='x', labelsize=16)
        ax.locator_params(nbins=5)
        #if i == 2: fig.colorbar(im[3], cax=ax, label="log(Number of Objects)")
        #plt.savefig("rc_%s.png" %names)
        #plt.close()

    #props = dict(boxstyle='round', facecolor='white')
    # axarr[0].text(
    #         0.5, 0.90, text, horizontalalignment='left', 
    #         verticalalignment='top', transform=axarr[0].transAxes, bbox=props,
    #         fontsize=16)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.1, 0.02, 0.8])
    cbar = plt.colorbar(im, cax=cbar_ax)
    #cbar.set_clim(0,12)
    cbar.set_label("Age [Gyr]", size=16)
    cbar.ax.tick_params(labelsize=16)

plt.show()
#plt.savefig("teff_logg_test_set.png")
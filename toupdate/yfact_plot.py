from pylab import *
import matplotlib.pyplot as plt

#This turns the standard deviation plotting on and off
standdev = True

tp_scale=max(hot_uA_mean)/max(max(hot_TP_mean),max(cold_TP_mean))

plt.clf()
rcParams['legend.fontsize'] = 10.0
fig, ax1 = plt.subplots()


ycut_low = where(mV_Yfactor < 1.0)
ycut_low_ind = ycut_low[0][-1]
ycut_high = where(mV_Yfactor > 2.5)
ycut_high_ind = ycut_high[0][0]


ax1.plot(mV_Yfactor, Yfactor, color="green", linewidth=3)
ax1.plot(mV_Yfactor[:ycut_low_ind], Yfactor[:ycut_low_ind], color="white", linewidth=4)
ax1.plot(mV_Yfactor[ycut_high_ind:], Yfactor[ycut_high_ind:], color="white", linewidth=4)
ax1.set_ylabel("Y factor", color="green")
ax1.set_ylim([-0.5, 2.5])
for tl in ax1.get_yticklabels():
    tl.set_color("green")

ax2 = ax1.twinx()
ax2.plot(hot_mV_mean, hot_uA_mean, color="red", linewidth=3)
ax2.plot(cold_mV_mean, cold_uA_mean, color="firebrick", linewidth=3, ls='dashed')
ax2.plot(hot_mV_mean, hot_TP_mean*tp_scale, color="purple", linewidth=3)
ax2.plot(cold_mV_mean, cold_TP_mean*tp_scale, color="blue", linewidth=3)
ax2.set_ylim([-10, 90])
ax2.set_ylabel('Current ($\mu$A)', color="firebrick")
for tl in ax2.get_yticklabels():
    tl.set_color('firebrick')


if standdev:
    # Positive sigma
    ax2.plot(hot_mV_mean, hot_uA_mean+hot_uA_std, color="red", linewidth=3, ls='dotted')
    ax2.plot(cold_mV_mean, cold_uA_mean+cold_uA_std, color="firebrick", linewidth=3, ls='dotted')
    ax2.plot(hot_mV_mean, (hot_TP_mean+hot_TP_std)*tp_scale, color="purple", linewidth=3, ls='dotted')
    ax2.plot(cold_mV_mean, (cold_TP_mean+cold_TP_std)*tp_scale, color="blue", linewidth=3, ls='dotted')

    # Negative sigma
    ax2.plot(hot_mV_mean, hot_uA_mean-hot_uA_std, color="red", linewidth=3, ls='dotted')
    ax2.plot(cold_mV_mean, cold_uA_mean-cold_uA_std, color="firebrick", linewidth=3, ls='dotted')
    ax2.plot(hot_mV_mean, (hot_TP_mean-hot_TP_std)*tp_scale, color="purple", linewidth=3, ls='dotted')
    ax2.plot(cold_mV_mean, (cold_TP_mean-cold_TP_std)*tp_scale, color="blue", linewidth=3, ls='dotted')




line1 = Line2D(range(10), range(10), color="red")
line2 = Line2D(range(10), range(10),color="green")
line3 = Line2D(range(10), range(10),color="purple")
line4 = Line2D(range(10), range(10),color="blue")
if standdev:
    line5 = Line2D(range(10), range(10),color="black", ls='dotted')
    plt.legend((line1,line2,line3,line4,line5),('IV Sweep','Y factor', '300K Total Power', '77K Total Power','1$\sigma$'),numpoints=1, loc=2)
else:
    plt.legend((line1,line2,line3,line4),('IV Sweep','Y factor', '300K Total Power', '77K Total Power'),numpoints=1, loc=2)



ax1.set_xlabel('Voltage (mV)')
#plt.ylabel('Current ($\mu$A)')
#show()
#savefig(plotdir+Ynum+".png")
savefig(plotdir+Ynum+".eps")

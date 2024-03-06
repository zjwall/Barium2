import nidaqmx
from nidaqmx import task 
# from nidaqmx.types import CtrTime
# nidaqmx.task.co_channels.add_co_pulse_chan_time("Dev1/ctr0")
# sample = CtrTime(high_time=0.001, low_time=0.001)
# nidaqmx.task.write(sample)
# nidaqmx.task.ao_channels.add_ao_voltage_chan("Dev1/ao0")   
# nidaqmx.task.write([1.1, 2.2, 3.3, 4.4, 5.5], auto_start=True)

# #task= Task()
# task.add_ao_voltage_chan('myDAQ1/ao0')
# test_Task.timing.cfg_samp_clk_timing(rate= 80, sample_mode= AcquisitionType.FINITE, samps_per_chan= 40)

# test_Writer = nidaqmx.stream_writers.AnalogSingleChannelWriter(test_Task.out_stream, auto_start=True)

# samples = np.append(5*np.ones(30), np.zeros(10))

# test_Writer.write_many_sample(samples)
# test_Task.wait_until_done()
# test_Task.stop()
# test_Task.close()
import matplotlib as plt
fig = plt.pyplot.fig()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

nfft = 1024
fs = 1000.0
freqs = np.linspace(0, fs/2, nfft/2+1)

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE, min_val=-5.0, max_val=5.0, units=VoltageUnits.VOLTS)
    task.timing.cfg_samp_clk_timing(fs, active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=nfft)

    # task.start()
    # task.stop()
    while True:

        t1 = (int(round(time.time() * 1000)))
        data = task.read(number_of_samples_per_channel=nfft)
        t2 = (int(round(time.time() * 1000)))
        tdata = np.array(data)
        tdata -= np.mean(tdata)
        ffto = np.fft.fft(tdata)
        ffto = np.abs(ffto)
        ffto = ffto[0:(nfft/2+1)]

        ax1.clear()
        ax2.clear()
        ax1.plot(data)
        ax2.plot(freqs, ffto)
        fig.show(0)
        plt.pause(0.000000001)
        t3 = (int(round(time.time() * 1000)))
        print('t2-t1 = {}ms, t3-t2 ={}ms').format(t2-t1, t3-t2)

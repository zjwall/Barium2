from artiq_config import config


print(config.DDS_dict)

for i in range(12):
    if i in config.DDS_dict.keys():
        print(config.DDS_dict[i][0], i)

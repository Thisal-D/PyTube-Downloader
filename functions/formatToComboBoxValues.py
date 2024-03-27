from .getConvertedSize import getConvertedSize


def formatToComboBoxValues(supported_download_types):
    reso_box_values = []
    for data_dict in supported_download_types:
        for data_key in data_dict:
            reso_box_values.append(data_key + " | " + getConvertedSize(data_dict[data_key] ,1))
    return (reso_box_values)
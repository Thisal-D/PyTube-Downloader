from .getConvertedSize import get_converted_size


def get_formated_combo_box_values(supported_download_types):
    combo_box_values = []

    for data_dict in supported_download_types:
        for data_key in data_dict:
            combo_box_values.append(data_key + " | " + get_converted_size(data_dict[data_key], 1))

    return combo_box_values

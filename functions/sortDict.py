def sort_dict(info: list[dict]) -> list[dict]:
    video_keys = []
    audio_keys = []
    for data in info:
        key = list(data.keys())[0]
        if "kbps" in key:
            audio_keys.append(key)
        else:
            video_keys.append(key)

    for i in range(len(video_keys)):
        for i2 in range(len(video_keys)-1):
            if int(video_keys[i2][:-1]) < int(video_keys[i2 + 1][:-1]):
                video_keys[i2], video_keys[i2+1] = video_keys[i2+1], video_keys[i2]

    keys = video_keys+audio_keys
    sorted_dict = []
    index2 = 0
    break_ = False
    while True:
        for dict_ in info:
            if list(dict_.keys())[0] == keys[index2]:
                sorted_dict.append(dict_)
                index2 += 1
                if index2 >= len(keys):
                    break_ = True
                    break
        if break_:
            break
                
    return sorted_dict

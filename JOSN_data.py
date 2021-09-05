import json
import os
import requests
import random
import numpy as np
import time
import csv
import re


def get_headers():
    """
    Random choose a header for requests.get() function
    :return: headers
    """
    USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC "
        "5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR "
        "2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR "
        "3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR "
        "2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET "
        "CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) "
        "Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 "
        "Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 "
        "TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 "
        "LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
        "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 "
        "LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
        "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
        "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; "
        "360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
        "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) "
        "Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 "
        "Safari/537.36",
    ]

    USER_AGENT = random.choice(USER_AGENT_LIST)
    headers = {'user-agent': USER_AGENT}
    return headers


def url_from_json(folder):
    """
    get useful video url from the json file
    :param folder: where you store your json file E.g /jan/Desktop/json_dir
    :return: video url list
    """
    requests.packages.urllib3.disable_warnings()
    url = []
    json_names = os.listdir(folder)
    json_names = [j for j in json_names if j.split(".")[-1] == "json"]

    for json_name in json_names:

        with open(os.path.join(folder, json_name)) as json_file:
            data = json.load(json_file)
            try:
                for j in range(len(data["mix_list"])):
                    try:
                        url.append(data["mix_list"][j]
                                   ["aweme_info"]["video"]["play_addr"]["url_list"][-2])
                    except:
                        pass
            except:
                pass

            try:
                length = len(data['aweme_list'])
            except:
                pass

            for i in range(length):
                try:
                    url.append(data['aweme_list'][i]
                               ['video']['play_addr']['url_list'][-2])
                except:
                    pass

        with open(os.path.join(folder, json_name)) as json_file:
            data = json_file.read()
            regex = '"(https://aweme.snssdk.com/aweme/v1/playwm/.*?)"'
            try:
                for u in re.findall(regex, data):
                    url.append(u)
            except:
                print("find no url from challenge")
    return url


def write_csv(dict_data, dst):
    """
    store the download information in a cvs file
    :param dict_data: a list ,every element is a dictionary
    :param dst: where your want to store your log file E.g /jan/Desktop/json_dir
    :return: None
    """

    csv_columns = ['Num', 'name', 'url', 'type', 'video_name']
    csv_file = "Summary.csv"
    csv_file = os.path.join(dst, csv_file)
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def download(parameter_list):
    """
    Prepare the download info and download the video from url
    :param parameter_list: a list
    parameter_list[0]: video url list we still needed to download
    parameter_list[1]: the total video url under challenge/user/sticker/music
    parameter_list[2]: path that you store your download video E.g /jan/Desktop/json_dir
    parameter_list[3]: video type challenge/user/sticker/music
    parameter_list[4]: video name E.g Gesture
    :return: None
    """

    length = len(parameter_list[0])
    dic_list = []
    dst = parameter_list[2] + "/"
    for j, u in enumerate(parameter_list[1]):
        video_id = u.split("=")[1].split("&")[0]
        data = dict()
        data['Num'] = j
        data['url'] = u
        data['type'] = parameter_list[3]
        data['name'] = parameter_list[4]
        data['video_name'] = video_id + ".mp4"
        dic_list.append(data)
    write_csv(dic_list, dst)

    for i, u in enumerate(parameter_list[0]):
        headers = get_headers()
        video_id = u.split("=")[1].split("&")[0]
        print(u)
        try:
            with open(dst + video_id + ".mp4", "wb") as f:
                im = requests.get(u, headers=headers, verify=False)
                print(im)

                f.write(im.content)
                print(
                    "{:.2f}% writing:{}".format(((i + 1) / length) * 100, dst + video_id + ".mp4"))

                time.sleep(random.uniform(0, 1))
        except:
            pass


def remove_repeat(parameter_list):
    """
    Remove already downloaded video url
    :param parameter_list: a list
    parameter_list[0]: the path that you store your json file
    parameter_list[0]: the path that you store your video file
    :return:
    url_unique: video url list we still needed to download
    url_unique1: the total video url under challenge/user/sticker/music
    """
    # parameter_list1 = [self.folder, self.dst]
    # video_url, all_url = remove_repeat(parameter_list1)
    alreadly = os.listdir(parameter_list[1])
    alreadly_name = [name.split(".")[0] for name in alreadly]

    url = url_from_json(parameter_list[0])
    print("url length:", len(url))

    url_unique1 = np.unique(url)
    url_unique = [ur for ur in url_unique1 if ur.split("=")[1].split("&")[0] not in alreadly_name]
    url_unique = np.sort(url_unique)
    print("unique url length:", len(url_unique))

    return url_unique, url_unique1


if __name__ == "__main__":
    """
    E.g
    """
    folder = "/Users/nebel/Desktop/2/我在抖音参加#百度回港上市challenge"
    dst = "/Users/nebel/Desktop/3/我在抖音参加#百度回港上市challenge"
    url, url1 = remove_repeat(folder, dst)
    download(url, url1, dst, "challenge", "我在抖音参加#百度回港上市")

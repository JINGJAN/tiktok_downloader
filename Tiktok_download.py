import urllib3
from JOSN_data import *
import re


def get_responses(get_responses_url):
    """
    Ignore the warnings
    :param get_responses_url: url we want to use get function
    :return: requests response
    """
    urllib3.disable_warnings()
    headers = get_headers()
    response = requests.get(get_responses_url, verify=False, headers=headers)
    return response


def get_redirect_url(share_url):
    """
    get redirect url
    :param share_url: url
    :return: redirected url
    """
    r = get_responses(share_url)
    return r.url


def genrate_letters():
    """
    generate signature for remaking url
    :return: signature
    """
    lt = []
    letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for l in letter:
        lt.append(l)
    text_signature = ''.join([random.choice(lt) for x in range(26)])
    return text_signature


def get_id(share_url):
    """
    get music id for remaking url
    :param share_url: Tiktok short url
    :return: musci id number
    """
    url = get_redirect_url(share_url)
    id_num = re.findall('(\d*)\?', url)[0]
    if id_num.isnumeric():
        return id_num
    else:
        print("Something wrong with id number")


def get_ch_id(share_url):
    """
    get challenge id for remaking url
    :param share_url: Tiktok short url
    :return: challenge id number
    """
    url = get_redirect_url(share_url)
    id_num = re.findall('/(\d*)/', url)[1]
    if id_num.isnumeric():
        return id_num
    else:
        print("Something wrong with id number")


def get_sec_id(share_url):
    """
    get security number
    :param share_url: redirected url
    :return: security number
    """
    regex = 'sec_uid=.*?&'
    out = re.findall(regex, share_url)[0]
    return out


class remake_url():
    """
    remake the json url from the shared url
    """
    def __init__(self, cursor):
        """
        initial parameter
        :param cursor: steps
        """
        self.cursor = cursor

    def remake_music_url(self, text_signature, music_id):
        """
        remake the music url
        :param text_signature: signature(total 26 characters)
        :param music_id: id number
        :return: url
        """
        text_head = "https://www.iesdouyin.com/web/api/v2/music/list/aweme/?"
        text_music_id = "music_id={}&".format(music_id)
        text_count = "count=36&"
        text_cursor = "cursor={}&".format(self.cursor)
        text_aid = "aid=1128&screen_limit=3&download_click_limit=0&_"

        remake = text_head + text_music_id + text_count + text_cursor + text_aid + text_signature
        return remake

    def remake_user_url(self, share_url):
        """
        remake the user url
        :param share_url: shared url
        :return: remake url
        """
        signature_list = ["ToWZhwAALto9c5Po75QH1k6FmZ", "OCp12QAAWHxL3H-2aPAunDgqdc", "U6o86AAAM.ogXDaHGe4txlOqPP",
                          "P0BGzAAAXyNMtkyjOHBM2z9ARt"]
        text_head = "https://www.iesdouyin.com/web/api/v2/aweme/post/?"
        text_mid = "count=21&"
        text_cursor = "max_cursor={}".format(self.cursor)
        text_sign = random.choice(signature_list)
        text_aid_sign = "&aid=1128&_signature=" + text_sign + "&dytk="
        text_sec_num = get_sec_id(share_url)
        remake = text_head + text_sec_num + text_mid + text_cursor + text_aid_sign
        return remake

    def remake_challenge_url(self, text_signature, ch_id):
        """
        remake the challenge url
        :param text_signature: signature
        :param ch_id: challenge id number
        :return: remake url
        """
        text_head = "https://www.iesdouyin.com/web/api/v2/challenge/aweme/?"
        text_music_id = "ch_id={}&".format(ch_id)
        text_count = "count=45&"
        text_cursor = "cursor={}&".format(self.cursor)
        text_aid = "aid=1128&screen_limit=3&download_click_limit=0&_"

        remake = text_head + text_music_id + text_count + text_cursor + text_aid + text_signature
        return remake

    def remake_sticker_url(self, st_id):
        """
        remake the sticker url
        :param st_id: sticker id number
        :return: remake url
        """
        text_head = "https://www.iesdouyin.com/web/api/v2/sticker/list/?"
        text_cursor = "cursor={}&".format(self.cursor)
        text_st_id = "sticker_id={}&count=15".format(st_id)

        remake = text_head + text_cursor + text_st_id
        return remake


class get_json(object):
    """
    get json file and store the file
    """
    def __init__(self, get_json_cursor, get_json_folder_path, already_exits_json, *args, **kwargs):
        """
        initial parameter
        :param get_json_cursor: step
        :param get_json_folder_path: json dir path
        :param already_exits_json: already exits json file
        :param args:
        :param kwargs:
        """
        self.get_json_cursor = get_json_cursor
        self.get_json_folder_path = get_json_folder_path
        self.already_exits_json = already_exits_json

    def write_json(self, name, dst_path, response):
        """
        write json file
        :param name: json we want to download
        :param dst_path: path to store the json file
        :param response: requests response
        :return: None
        """
        if name in self.already_exits_json:
            print("{} was already exit".format(name))
            return -1
        else:
            with open(dst_path, "w") as write_file:
                json.dump(response.json(), write_file)
                print("Writing {}".format(dst_path))

    def return_response(self, response, get_json_id_num):
        """
        whether reach the end of challenge/user/sticker/music
        :param response: requests response
        :param get_json_id_num: step
        :return: True/False bool
        """
        if response.status_code == 200:
            has_more = True
            self.write_json_music(get_json_id_num, response)
            json_string = response.json()
            if 'has_more' in json_string:
                has_more = json_string['has_more']
            return has_more
        else:
            raise Exception("Sorry")

    def write_json_music(self, get_json_id_num, response):
        """
        store the music json file
        :param get_json_id_num: step
        :param response: requests response
        :return:
        """

        name = str(get_json_id_num) + "_" + str(self.get_json_cursor) + ".json"
        dst_path = os.path.join(self.get_json_folder_path, name)
        self.write_json(name, dst_path, response)

    def write_json_user(self, response):
        """
        store the user json file
        :param response:
        :return:
        """

        name = str(self.get_json_cursor) + ".json"
        dst_path = os.path.join(self.get_json_folder_path, name)
        self.write_json(name, dst_path, response)

    def get_json_info_music(self, get_json_id_num):
        """
        store the music json file
        :param get_json_id_num:
        :return:
        """
        signature = genrate_letters()
        remake = remake_url(self.get_json_cursor)
        json_url = remake.remake_music_url(signature, get_json_id_num)

        response = get_responses(json_url)

        return self.return_response(response, get_json_id_num)

    def get_json_info_user(self, share_url):
        """
        store the user json file
        :param share_url:
        :return:
        """
        remake = remake_url(self.get_json_cursor)
        json_url = remake.remake_user_url(share_url=share_url)

        response = get_responses(json_url)

        if response.status_code == 200:
            has_more = True
            cursor = None
            self.write_json_user(response)
            json_string = response.json()

            if 'has_more' in json_string and 'max_cursor' in json_string:
                has_more = json_string['has_more']
                cursor = json_string['max_cursor']
            return has_more, cursor
        else:
            raise Exception("Sorry")

    def get_json_info_sticker(self, st_id):
        """
        store the sticker json file
        :param st_id:
        :return:
        """
        remake = remake_url(self.get_json_cursor)
        json_url = remake.remake_sticker_url(st_id)
        response = get_responses(json_url)
        return self.return_response(response, st_id)


class Download(object):
    """
    Download the Ticktok Video
    """

    def __init__(self, download_url, download_folder, download_dst, specific_type, name):
        """
        initial parameters
        :param download_url: video url
        :param download_folder: json dir
        :param download_dst: video dir
        :param specific_type: video type
        :param name: video name
        """
        self.url = download_url
        self.folder = download_folder
        self.dst = download_dst
        self.specific_type = specific_type
        self.name = name

    def download_configure(self):
        """
        :return:
        """
        parameter_list1 = [self.folder, self.dst]
        video_url, all_url = remove_repeat(parameter_list1)
        parameter_list = [video_url, all_url, self.dst, self.specific_type, self.name]
        download(parameter_list)

    def download_specific_music_challenge(self, step, music_or_ch):
        """
        download music/challenge videos
        :param step: step
        :param music_or_ch: video type
        1: download music
        2: download challenge
        :return: None
        """

        if music_or_ch == 1:
            id_num = get_id(self.url)
        # get Challenge id number
        if music_or_ch == 2:
            id_num = get_ch_id(self.url)

        cursor = 0
        already = os.listdir(self.folder)

        while True:
            music_info = get_json(cursor, self.folder, already)
            has_more = music_info.get_json_info_music(id_num)
            if not has_more:
                print("Reach the end")
                break
            cursor += step
            print("wait seconds")
            time.sleep(random.uniform(2, 3))

        self.download_configure()

    def download_specific_user(self):
        """
        download user videos
        :return: None
        """

        cursor = 0
        already = os.listdir(self.folder)

        while True:
            user_info = get_json(cursor, self.folder, already)
            new_url = get_redirect_url(self.url)
            has_more, cursor_next = user_info.get_json_info_user(new_url)
            if not has_more:
                print("Reach the end")
                break
            if cursor_next is not None:
                cursor = cursor_next
            if cursor_next is None:
                cursor += 50
            print("wait seconds")
            time.sleep(random.uniform(2, 3))

        self.download_configure()

    def download_specific_sticker(self, step):
        """
        Download sticker videos
        :param step: step
        :return: None
        """

        st_id = get_ch_id(self.url)
        cursor = 0
        already = os.listdir(self.folder)

        while True:
            music_info = get_json(cursor, self.folder, already)
            has_more = music_info.get_json_info_sticker(st_id)
            if not has_more:
                print("Reach the end")
                break
            cursor += step
            print("wait seconds")
            time.sleep(random.uniform(2, 3))

        self.download_configure()


def main(args):
    if args[3] == "music":
        downloader = Download(args[0], args[1], args[2], args[3], args[4])
        downloader.download_specific_music_challenge(step=36, music_or_ch=1)
    if args[3] == "challenge":
        downloader = Download(args[0], args[1], args[2], args[3], args[4])
        downloader.download_specific_music_challenge(step=45, music_or_ch=2)
    if args[3] == "user":
        downloader = Download(args[0], args[1], args[2], args[3], args[4])
        downloader.download_specific_user()
    if args[3] == "sticker":
        downloader = Download(args[0], args[1], args[2], args[3], args[4])
        downloader.download_specific_sticker(step=30)

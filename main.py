import os
import argparse
from Tiktok_download import main
import multiprocessing
from JOSN_data import download, remove_repeat


def argument_parameters(text_path, json_path, output_path):
    """
    Parsing the txt file prepare the parameters for download
    :param text_path: txt file path E.g /Users/jan/Desktop/Download.txt
    :param json_path: path that you want to create your json dir
    :param output_path: path that you want to create your video dir
    :return:
    argument_list[0]: the whole videos urls under challenge/user/sticker/music
    argument_list[1]: the path of json dir we created
    argument_list[2]: the path of video dir we created
    argument_list[3]: type of video challenge/user/sticker/music
    argument_list[4]: name of video
    """
    with open(text_path, 'r') as f:
        lines = f.readlines()
    argument_list = []
    out_dir_list = []

    for line in lines:

        line = line.strip("\n")
        list_line = line.split(",")
        share_url = list_line[0]
        name = list_line[1]
        specific_type = list_line[2]

        json_dir = os.path.join(json_path, name + specific_type)
        out_dir = os.path.join(output_path, name + specific_type)

        try:
            os.mkdir(json_dir)
            os.mkdir(out_dir)
            print("making json_dir {} and out_dir {}".format(json_dir, out_dir))
        except:
            pass
        argument_list.append([share_url, json_dir, out_dir, specific_type, name])
        out_dir_list.append(out_dir)

    return argument_list, out_dir_list


def upload_Tiktok_video_cmd(source, dest):
    """
    Upload video to boss path cv_platform/jan/tmp/ + dest
    :param source: local path that we store the video
    :param dest: new video dir under cv_platform/jan/tmp/
    :return: None
    """
    bucket_name = "cv_platform" + "/jan/tmp/"
    endpoint = "http://jssz-boss.bilibili.co"

    os.system("aws --endpoint-url=" + endpoint + " s3 cp " + source +
              " s3://" + bucket_name + dest + " --recursive")


def upload_video(out_dir_list):
    """
    Upload video to boss
    :param out_dir_list: Videos dir names
    :return: None
    """
    for out_dir in out_dir_list:
        subname = out_dir.split("/")[-1]
        name = args.output_path.split("/")[-1]
        dst_name = os.path.join(name, subname)
        upload_Tiktok_video_cmd(out_dir, dst_name)


if __name__ == "__main__":
    # define cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', type=str, help='path of output video')
    parser.add_argument('--json-path', type=str, help='path of output json')
    parser.add_argument('--text-path', type=str, help='path of text')
    parser.add_argument('--direct-download', type=str, help='direct download', default=None)
    args = parser.parse_args()

    argument_list, out_dir_list = argument_parameters(args.text_path, args.json_path, args.output_path)

    if args.direct_download is None:
        p = multiprocessing.Pool(4)

        p.map(main, argument_list)

        # upload_video(out_dir_list)

    else:
        print("direct download video from json")
        download_list = []
        for i, element in enumerate(out_dir_list):
            url_unique, url_unique1 = remove_repeat([argument_list[i][1], element])
            download_list.append([url_unique, url_unique1, element, argument_list[i][3], argument_list[i][4]])

        p = multiprocessing.Pool(4)
        p.map(download, download_list)
        # upload_video(out_dir_list)

import speedtest as st

'''
一种简单的方式，使用python测试下载/上传网络

pip install speedtest-cli
'''


def speed_test():
    test = st.Speedtest()

    download_speed = test.download()
    download_speed = round(download_speed / 10 ** 6, 2)
    print('download speed is: {} Mbps'.format(download_speed))

    upload_speed = test.upload()
    upload_speed = round(upload_speed / 10 ** 6, 2)
    print('upload speed is: {} Mbps'.format(upload_speed))

    ping = test.results.ping
    print('ping: ', ping)


if __name__ == '__main__':
    for i in range(1, 6):
        print('the {} times, test result: '.format(i))
        speed_test()

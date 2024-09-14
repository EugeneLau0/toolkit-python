'''
在X上看到的一道题，留言区发现有许多不同的答案，于是自己来验证下

https://x.com/clcoding/status/1834774362764812333

最终在macOS的3.9版本下，得到的结果为：
2
3
'''
if __name__ == '__main__':
    number = 100
    if number == 50:
        print('1')
    else:
        print('2')
        if number == 100:
            print('3')

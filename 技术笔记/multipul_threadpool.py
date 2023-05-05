import time
import threading


def matter1(music, test):
    print(test, music)
    time.sleep(2)
    print('matter1 stop')
    # 假设每一首歌曲的时间是2秒

def matter2(music, test):
    print(test, music)
    time.sleep(1)
    print('matter2 stop')
    # 假设每一首歌曲的时间是2秒

if __name__ == '__main__':
    # 设定我要听的歌为
    musics = ["music1", "music2", "music3"]
    test = "122678"
    # 开始时间
    start = time.time()

    threadpool = []

    for music in musics:
        th = threading.Thread(target=matter1, args=(music, test))
        threadpool.append(th)
    for th in threadpool:
        th.start()
    for th in threadpool:
        # 自闭
        threading.Thread.join(th)

    threadpool2 = []
    for music in musics:
        th = threading.Thread(target=matter2, args=(music, test))
        threadpool2.append(th)
    for th in threadpool2:
        th.start()
    for th in threadpool2:
        # 自闭
        threading.Thread.join(th)

    # 结束时间
    end = time.time()
    print("完成的时间为：" + str(end - start))
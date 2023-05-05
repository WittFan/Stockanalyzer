# 多线程
```python
import threading
th = threading.Thread(target=matter2, args=(music, test))
th.start()
```
threading.Thread.join(th)为自闭方法，再th运行完后再运行后面的程序。

```python
import time
import threading


def matter1(music, test):
    print test, music
    # 假设每一首歌曲的时间是2秒
    time.sleep(2)


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

    # 结束时间
    end = time.time()
    print("完成的时间为：" + str(end - start))
```
## 线程里再开线程
```python
#这个demo程序证明了线程之内还可以再创造线程。
import threading
import time
 
def  run(shijian):
    time.sleep(shijian)
    print("等待了 " ,shijian,"秒，函数执行完毕")
 
def  demo(shijian1,shijian2):
    t1 = threading.Thread(target=run, args=(shijian1,))
    t2=threading.Thread(target=run,args=(shijian2,))
    try:
        t1.start()
    except:
        print("t1执行有问题")
    t2.start()
 
 
 
t=threading.Thread(target=demo,args=(6,3))
t.start()
print("  hello ,world")
```
执行的结果是：\
 hello ,world\
等待了  3 秒，函数执行完毕\
等待了  6 秒，函数执行完毕\
进程已结束,退出代码0\
这就证明了hello，world先打印出来，主线程 t，是正确执行的。\
t之内的  线程  t1,t2     其中t2是先打印出来的。  那么t1,t2这两个线程也是正确工作的。
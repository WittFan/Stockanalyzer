# concurrent

## 好处
那么已经有threading、multiprocess了，为什么还要整出一个concurrent.futures呢？
concurrent.futures主要实现了进程池和线程池，适合做派生一堆任务，异步执行完成后，再收集这些任务，且保持相同的api，池的引入带来了一定好处：
1.程序猿开发更快，代码简洁，调调函数
2.进程线程复用，减去了大量开辟、删除进程线程时的开销
3.有效避免了因为创建进程线程过多，而导致负荷过大的问题

## 机制
内部实现机制非常复杂，简单来说就是开辟一个固定大小为n的进程池/线程池。
进程池中最多执行n个进程/线程，当任务完成后，从任务队列中取新任务。
若池满，则排队等待。

## Excecutor
ThreadPoolExecutor和ProcessPoolExecutor都继承于Executor，该抽象类提供异步执行调用方法。
### 构造函数参数：
ThreadPoolExecutor(max_workers=None)\
ProcessPoolExecutor(max_workers=None)\
max_workers：就是池的大小，可以容纳的进程或线程数量。为None则默认为cpu核数。
线程池大小可以大于cpu核数，进程池大小建议要小于等于进程池核数。\

### 方法
* map(func,*iterables,timeout=None,chunksize=1)：很常用！！\
参数：主要提一点chunksize，将iterables分割成chunksize个任务块并作为独立的任务并提交到执行池中。
对很长的迭代器来说，使用大的chunksize值比默认值 1 能显著地提高性能。该参数只对进程池有效，线程池无效
跟内置map很像，对序列执行相同操作，是异步执行的、非阻塞。\
返回的是一个生成器，可以遍历该生成器得到结果，注意不论执行完成的先后顺序如何，
遍历该生成器返回的顺序永远是输入参数iterator的顺序。
与multiprocessing.Pool中的方法区分，concurrent.futures中的map方法是异步执行的，
且返回的是生成器，而multiprocessing.Pool返回的直接是结果组成的list。
* submit(fn,/,*args,**kwargs)
将fn加入池中，以 fn(*args **kwargs) 方式执行并返回Future对象封装该函数的执行。
例子
```python
with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(pow, 323, 1235)
    print(future.result())
```
* shutdown(wait=True,*,cancel_futures=False)
先判断是否要关闭（比如看池中future对象是否全执行完成），再释放使用的任何资源。
若在关闭后调用map，submit方法，则报runtimeerror。\
参数：\
wait 为 True，等待所有future执行完成再释放；wait 为 False，执行到该shutdown语句就立即释放。
不论wait取值，整个 Python 程序将等到所有待执行的 future 对象完成执行后才退出。
cancel_futures 为 True，此方法将取消所有执行器还未开始运行的挂起的 Future。
任何已完成或正在运行的 Future 将不会被取消，无论 cancel_futures 的值是什么。
* with语句
避免显式调用shutdown方法。
```python
with futures.ThreadPoolExecutor(3) as executor:
    future = executor.submit(pow, 323, 1235)
    print(future.result())
    # 调用executor.shutdown(wait=True)，在所有线程都执行完毕前阻塞当前线程
```
* map
再看个长一点的例子：
```python
from concurrent import futures
import time
import random

def returnNumber(number: int) -> int:
    print("start threading {}".format(number))
    time.sleep(random.randint(0, 2))  # 随机睡眠
    print("end threading {}".format(number))
    return number  # 返回参数本身

if __name__ == '__main__':
    with futures.ThreadPoolExecutor(3) as executor:
        # with语句会调用executor.shutdown(wait=True)，在所有线程都执行完毕前阻塞当前线程
        res = executor.map(returnNumber,range(0, 5))
        # 返回一个生成器，遍历的结果为0,1,2,3。无论执行结果先后顺序如何，看输入的iterator顺序
        # 因为线程池为3，所以0~2进池，其中某个执行完后，3进池
        print(res)
    print("----print result----")
    for r in res:
        print(r)
```
## future类
future？可以理解为还未完成的任务，future封装了待完成的任务，
实现了主进程和子进程之前的通信，比如查询完成状态，得到结果。

Future
将函数封装为异步执行，可以理解为还未完成的任务，future封装了待完成的任务，实现了主进程和子进程之前的通信，比如查询完成状态，得到结果。不建议自己定义一个Future，Future实例应该由Executor.submit()创建，由执行器来管理。

classconcurrent.futures.Future

方法：
cancel()：尝试取消调用。 如果调用正在执行或已结束运行不能被取消则该方法将返回 False，
否则调用会被取消并且该方法将返回 True。\
cancelled()：如果调用成功取消返回 True。\
running()：如果调用正在执行而且不能被取消那么返回 True 。\
done()：如果调用已被取消或正常结束那么返回 True。常用\
result(timeout=None)\
返回执行函数的返回值。如果调用还没完成那么这个方法将等待 timeout 秒。
如果在 timeout 秒内没有执行完成，concurrent.futures.TimeoutError将会被触发。
timeout 可以是整数或浮点数。
如果 timeout 没有指定或为 None，那么等待时间就没有限制。\
如果 futrue 在完成前被取消则CancelledError将被触发。\
如果调用引发了一个异常，这个方法也会引发同样的异常。\
exception(timeout=None)\
返回由调用引发的异常。如果调用还没完成那么这个方法将等待 timeout 秒。\
如果在 timeout 秒内没有执行完成，concurrent.futures.TimeoutError将会被触发。\
timeout 可以是整数或浮点数。如果 timeout 没有指定或为 None，那么等待时间就没有限制。\
如果 futrue 在完成前被取消则CancelledError将被触发。\
如果调用正常完成那么返回 None。\
add_done_callback(fn)\
当 future 对象被取消或完成运行时，将会调用 fn，并且传入参数future对象 （也是唯一的参数）。\
# 例子
```python
from concurrent.futures import ThreadPoolExecutor
import requests

def get_context(url):
    res = requests.get(url).text
    return {'url': url, 'res': res}

def parse_context(future):
    # 参数就是get_context结果的future对象，必须要拿到结果
    result = future.result()
    with open('a.txt', 'a', encoding='utf-8') as f:
        f.write('%s-%s\n' % (result['url'], len(result['res'])))


if __name__ == '__main__':
    urls = [
        'http://www.openstack.org',
        'https://www.python.org',
    ]
    t = ThreadPoolExecutor()
    for url in urls:
        t.submit(get_context, url).add_done_callback(parse_context) # 在执行完get_context后执行parse_context，实现同步
```

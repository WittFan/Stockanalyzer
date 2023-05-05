

### 将文件夹.idea从git cached中删除
git rm --cached -r .idea

### 使用Shadowsocks代理
利用shadowsocks的socks5代理，配置好后明显加速。
用下面两条命令配置好后，保持shadowsocks客户端开启就行了。
```shell
git config --global http.proxy 'socks5://127.0.0.1:1080' 
git config --global https.proxy 'socks5://127.0.0.1:1080'
```
shadowsocks的本地端口默认是1080 
上面设置只是开启https://代理
git开启http/https代理详解
```shell
# 查看git 可以配置的内容
git config
# 部分配置内容详解
global  即是读/写当前用户全局的配置文件(~/.gitconfig 文件，属于某个计算机用户)
system  即是读写系统全局的配置文件(/etc/gitconfig 文件，属于计算机)
local   即是当前 clone 仓库 的配置文件(位于 clone仓库下 .git/config)。
blob    配置是另外一种形式，提供一个 blob 大对象格式，没有验证过，估计与 local 是一样的，只是形式不同。

# 查看当前代理设置
git config --global http.proxy
git config --global https.proxy

# 设置当前代理为 http://127.0.0.1:1080 或 socket5://127.0.0.1:1080
git config --global http.proxy 'http://127.0.0.1:1080'
git config --global https.proxy 'https://127.0.0.1:1080'

git config --global http.proxy 'socks5://127.0.0.1:1080'
git config --global https.proxy 'socks5://127.0.0.1:1080'

# 删除 proxy
git config --global --unset http.proxy
git config --global --unset https.proxy
```
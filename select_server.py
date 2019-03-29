from select import select 
from socket import *

# 创建套接字作为关注IO
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(5)

# 添加关注列表
rlist = [s]
wlist = []
xlist = [s]

while True:
    # 监控关注的IO
    rs,ws,xs = select(rlist,wlist,xlist)

    #遍历三个列表，确定IO进行处理
    for r in rs:
        if r is s: 
            c,addr = r.accept()
            print("Connect from",addr)
            rlist.append(c) #添加新的关注
        # 服务端接收到了消息
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                r.close()
                continue
            print(data.decode())
            # 将r加入到主动处理列表，表示要主动处理
            wlist.append(r)

    for w in ws:
        w.send(b'OK')
        wlist.remove(w)

    for x in xs:
        if x is s:
            x.close()
            



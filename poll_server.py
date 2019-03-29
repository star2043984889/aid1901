from select import*
from socket import*



#创建关注ＩＯ
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',9809))
s.listen(5)


#创建poll对象
p = poll()



#建立查找字典
fdmap = {s.fileno():s}




# 关注套接字

p.register(s,POLLIN|POLLERR)


#循环监控ＩＯ
while True:
    events = p.poll()  #阻塞等待ＩＯ发生
    #遍历列表处理ＩＯ
    for fd,event in events:
        if fd == s.fileno():
            c,addr = fdmap[fd].accept()
            print('connect from',addr)

            #注册新ＩＯ
            p.register(c,POLLIN|POLLERR)
            fdmap[c.fileno()] = c
        elif  event & POLLIN:
            data = fdmap[fd].recv(1024)
            if not data:
                p.unregister(fd)  #取消关注
                fdmap[fd].close()
                del fdmap[fd] #从字典删除
                continue
            print(data.decode())
            fdmap[fd].send(b'ok')
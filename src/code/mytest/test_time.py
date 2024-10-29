import json
import time

#f1，f2测试不同加载jsonl的方式时间区别
def f1(path):
    s1=time.time()
    data=[]
    with open(path, 'r') as f:
        data = [json.loads(line) for line in f]
    s2=time.time()
   # print(s2-s1)
    return data

def f2(path):
    s1=time.time()
    with open(path, 'r') as f:
        data=f.read()
        datas=data.splitlines()
        lines = [json.loads(line) for line in datas]
    s2=time.time()

# f3，f4不同jsonl写的方式的时间区别
def f3(pathin,pathout):
    s1=time.time()
    l=f1(pathin)
    with open(pathout, 'w') as f:
        for line in l:
            line["llllll"]="我准备好了哈哈哈哈哈哈哈哈哈哈哈"
            json.dump(line, f)
            f.write("\n")
    s2=time.time()
    print(s2-s1)
    print("\n")

def f4(pathin,pathout):
    s1=time.time()
    l=f1(pathin)
    with open(pathout, 'w') as f:
        l=[json.dumps(line) for line in l]
        f.write("\n".join(l))
    s2=time.time()
    print(s2-s1)

# f5，f6是不同字符拼接的方式的时间区别
def f5(pathin,pathout):
    s1=time.time()
    l=f1(pathin)
    with open(pathout, 'w') as f:
        for line in l:
            line["llllll"]=line["instruct"]+line["input"]
            json.dump(line, f)
            f.write("\n")
    s2=time.time()
    print(s2-s1)
    print("\n")

def f6(pathin,pathout):
    s1=time.time()
    l=f1(pathin)
    with open(pathout, 'w') as f:
        for line in l:
            line["llllll"]=line["instruct"].join(line["input"])
            json.dump(line, f)
            f.write("\n")
    s2=time.time()
    print(s2-s1)
    print("\n")



if __name__ == '__main__':
    f5("../../data/3_QA_2/English.jsonl","./ccc.jsonl")

    f6("../../data/3_QA_2/English.jsonl","./ddd.jsonl")



#f1，f2都在0.0074秒左右
#总结，对于1M的文件读写速度影响不大

#对于jsonl文件一次性将文件写，确定比遗憾一行一行写快很多，快1/4，如果文件更大可能更明显。
#但是对于小文件1M的影响不大

# 少量字符拼接，+反而明显优于join
# ai4s

高考试卷测评

## 第一次数据处理说明

others是参考的别人的代码，基本没用，主要看src中的

其中处理好的数据放在了data_processed文件下，里面的数据包含9个学科

0_raw_data_process.py 数据处理为json

1_QA_data_peocess.py 数据处理为指令数据集，仅包含简单的prompt(后续不会使用，初级版本)

2_infer.py 简单推理，简单的prompt，没有规定格式(后续不会使用，初级版本)

3_QA_data_2_process.py 数据处理为包含复杂规范的prompt

4_infer_2_res 用复杂规范的prompt进行推理获取答案

5.对推理结果分析

6.通过调用api方式进行推理

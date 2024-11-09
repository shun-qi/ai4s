# ai4s

高考试卷测评

# 项目结构说明

其中处理好的数据放在了data文件下

other是gaokaobench代码与数据集，做参考。主要还是看src中的代码和数据


code文件夹下

0_raw_data_process.py 数据处理为json

1_QA_data_peocess.py 数据处理为指令数据集，仅包含简单的prompt(后续不会使用，初级版本)

2_infer.py 简单推理，简单的prompt，没有规定格式(后续不会使用，初级版本)

3_QA_data_2_process.py 数据处理为包含复杂规范的prompt

4_infer_2_res 用复杂规范的prompt进行推理获取答案（推理的函数第一个版本）

5_infer_with_api通过api与本地的方式调用大模型进行推理

6_analysis通过调用本地部署的qwen-2-72B对推理结果打分

7与9是图片生成的代码

8是不同prompt结果的打分代码


data文件下

0_raw是对试卷的提取结果

1_QA是将数据处理为简单的指令问答格式

2_infer_res是简单指令问答的推理结果

3_QA_2是复杂prompt的指令问答格式

4_infer_2_res是各个大模型推理结果

5_analysis是各个大模型推理结果的打分

6_graphs是图表

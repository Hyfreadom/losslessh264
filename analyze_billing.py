#!/usr/bin/python
#用于指定python解释器，此处为Ubuntu自带的解释器
import argparse

_cmdline_desc = """\
Analyze output of rountrip tests.

First run: roundtriptest/run.sh &> output
Then pass output as an argument to this script.
"""

_cmdline_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,   #保留帮助信息的空白和缩进
    description='Analyze output of h264dec')                #--help中显示的帮助信息
_cmdline_parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',                                    #出现v的时候将该参数(v)设为True
    help='Print debugging statements.',
)
_cmdline_parser.add_argument(
    'output_path',                                          #output_path = $bill，bill是一个log数据，与report内容一致
    type=str,
    help='Path to stdout file capture of h264dec.',
)


from collections import OrderedDict #collection提供了一些容器类型，包括defaultdict和OrderDict
# 具体来讲，OrderedDict 是一种有序字典，它保留了添加键的顺序，这使得 OrderedDict 更适合于需要维护元素插入顺序的场景，而不是键自然排序的场景。
# 与普通的字典不同，它的键值对的顺序是按照添加顺序来维护的。

import re               #用于正则表达式匹配
#re.compile
feature_bill_re = re.compile(r'^(?P<index>\d*)\s*::\s*(?P<bytes>\d+(.\d+)?)\s*\[(?P<label>.*)\]')
# 匹配诸如    123 :: 45.67 [label]  的结果，123表示整数存入idex，45.67表示浮点数存入bytes，label表示一个字符串
# 具体如下
# ?P<xxx>用于制定一个名为xxx的捕获组，以此通过名称引用捕获组，而不是组号
# \d 表示一个数字，\s表示一个空白字符
# .                     # 匹配除换行字符外的任意字符
# *                     # 匹配前面的元素任意次
# +                     # 匹配前面的元素1次或多次
# ？                    # 匹配前面的元素0词或1词
# ^                     # 匹配行的开头
# (?P<index>\d*)        # 匹配零个或多个数字，保存在名为index的分组中
# \s*::\s*              # 匹配两个冒号及其周围的任意空白字符
# (?P<bytes>\d+(.\d+)?) # 匹配一个或多个数字，可能包含一个小数点和更多数字，保存在名为bytes的分组中
# \s*\[                 # 匹配任意空白字符和一个左中括号
# (?P<label>.*)\]       # 匹配一个或多个任意字符，保存在名为label的分组中，直到遇到右中括号为止


#HEADER是一个元组，用于打印表头，结合下面用字符串写的定义，最终print的表头结果如下
#                     Feature      Bench       Ours        O-B        O/B%
HEADER = ('Feature', 'Bench', 'Ours', 'O-B', 'O/B') 
#{:>22}表示22位宽右对齐字符串，{:>10}表示10位宽右对齐字符串 {:>10}%表示10位宽右对齐字符串，用%结尾  {:>10,}表示10位宽右对齐字符串并用，做千位分隔符
header_row_format = '{:>22} {:>10} {:>10} {:>10} {:>10}%'       
feature_row_format = '{:>22} {:>10,} {:>10,} {:>10,} {:>10}%'   

class VideoCompressionResult(object):
    def __init__(self, name):
        self.name = name
        self.ours = OrderedDict()                       #字典，且按键的插入顺序进行迭代
        self.benchmark = OrderedDict()                  #字典，且按键的插入顺序进行迭代
    def __repr__(self):                                 #返回对象的表示形式，在print的时候返回名称而非地址
        return 'VideoCompressionResult(%r)' % self.name # %r表示self.name的字符串表示形式

 # parse_outputs 用于处理二次压缩过程生成的bill文件，解析bill文件中的内容，获取其中的nonzeros和compressed bytes等信息
 # 返回值为一个含有VideoCompressionResult对象的列表，该对象含有ours属性或benchmark属性
def parse_outputs(output_path):                         
    video_files = []
    video_result = VideoCompressionResult('video file') #实例化一个name属性为video file的VideoCompressionResult对象
    video_results = [video_result]
    with open(output_path, 'r') as output_file:
        for line in output_file:                        #output_file 为 bill（report）文档
            if line.startswith('==='):                  #判断是否为==开头（==开头说明是分割行，包含表头信息）
                video_name = line.strip(' =\n')         #提取表头中的名称信息(去除=和空格)，作为video name
                video_files.append(video_name)          #将video name作为字符接入video_files列表
                video_result = VideoCompressionResult(video_name)   #用video name创建一个VideoCompressionResult实例
                video_results.append(video_result)      #将video name 的实例接入video_results列表
                continue
            m = feature_bill_re.match(line.strip())     # m表示正则表达式匹配，匹配成功则返回对象，否则是None
            if m:                                       # 判断是否是压缩信息
                label = m.groupdict()['label']          # 返回所有键为label的键值对
                if '.' in m.groupdict()['bytes']:       # 检查捕获到的bytes的键值对中的 键 是否包含小数点
                    #将包含小数点的键值中的浮点数字符串转为整数，并作为键值，label作为键，存入benchmark字典
                    video_result.benchmark[label] = int(float(m.groupdict()['bytes']))  
                else:
                    #将不包含小数点的键值中的整数字符串转为整数，  并作为键值，label作为键，存入ours字典
                    video_result.ours[label] = int(m.groupdict()['bytes'])
                continue
    return [video_result for video_result in video_results      #返回值为一个含有VideoCompressionResult对象的列表
            if video_result.ours or video_result.benchmark]

def perc(num, denom):       #计算 num/denom 的百分比
    if denom == 0:
        return float('inf')
    else:
        return int(round(100 * float(num) / denom))

def analyze(output_path):
    video_results = parse_outputs(output_path)          
    for video_result in video_results:
        print 'Analysis of %s' % video_result.name
        print '\t' + header_row_format.format(*HEADER)  
#打印的表头如下所示
#Analysis of xxxx
#                     Feature      Bench       Ours        O-B        O/B%
        # Combine the label lists preserving order.
        ours_labels = {k:i for i, k in enumerate(video_result.ours.keys())}
        benchmark_labels = {k:i for i, k in enumerate(video_result.benchmark.keys())}
        def order(a, b):
            if a in ours_labels and b in ours_labels:
                return cmp(ours_labels[a], ours_labels[b])
            if a in benchmark_labels and b in benchmark_labels:
                return cmp(benchmark_labels[a], benchmark_labels[b])
            return 0
        labels = sorted(set(ours_labels) | set(benchmark_labels), cmp=order)

        for label in labels:
            bench = video_result.benchmark.get(label, 0)
            us = video_result.ours.get(label, 0)
            print '\t' + feature_row_format.format(label, bench, us, us - bench, perc(us, bench))

        for prefix in 'luma ', 'chroma ', 'pred ', '':
            def total(table):
                return sum(v for k, v in table.items() if k.startswith(prefix))
            bench = total(video_result.benchmark)
            us = total(video_result.ours)
            print '\t' + feature_row_format.format(
                    '{}total:'.format(prefix), bench, us, us - bench, perc(us, bench))

        print ''
    return video_results
'''打印的表格示例
Analysis of video file
	               Feature      Bench       Ours        O-B        O/B%
	           boilerplate        259        847        588        327%
	                  skip      3,506      3,033       -473         87%
	              skip end          0        253        253        inf%
	                  cbpl      9,300      7,871     -1,429         85%
	                   qpl      1,612        352     -1,260         22%
	               mb type      4,622      3,714       -908         80%
	                   ref          0        103        103        inf%
	              pred 8x8        183      1,290      1,107        705%
	            pred 16x16      4,579        408     -4,171          9%
	             pred mode      6,171      9,411      3,240        153%
	                sub mb        333         30       -303          9%
	                 mv[0]     11,512     10,688       -824         93%
	                 mv[1]     10,976     10,239       -737         93%
	               luma dc      2,737        666     -2,071         24%
	             chroma dc      1,999      1,678       -321         84%
	            luma 0 eob     45,747     22,208    -23,539         49%
	        luma 0 bitmask      2,012      6,347      4,335        315%
	       luma 0 exponent          0          7          7        inf%
	    luma 0 significand      1,563      4,304      2,741        275%
	           luma 0 sign      4,940      4,351       -589         88%
	      luma Nth bitmask      3,417     13,469     10,052        394%
	     luma Nth exponent          0          2          2        inf%
	  luma Nth significand      1,006      3,774      2,768        375%
	         luma Nth sign      6,908      6,678       -230         97%
	            chroma eob         64         48        -16         75%
	        chroma bitmask          0         13         13        inf%
	            chroma exp          0          1          1        inf%
	    chroma significand          0          7          7        inf%
	           chroma sign         11         12          1        109%
	              pad byte          0         34         34        inf%
	           luma total:     68,330     61,806     -6,524         90%
	         chroma total:      2,074      1,759       -315         85%
	           pred total:     10,933     11,109        176        102%
	                total:    123,457    111,838    -11,619         91%

'''


def main():
    parsed_args = _cmdline_parser.parse_args()
    return analyze(parsed_args.output_path)

if __name__ == '__main__':
    video_results = main()


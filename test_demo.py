import re
########################比较report 与 bill 文件是否相同##########################
def compare_files(file1_path, file2_path):      #比较report 与 bill 文件是否相同
    with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
        while True:
            f1_chunk = f1.read(1024)
            f2_chunk = f2.read(1024)
            if f1_chunk != f2_chunk:
                print('Files are different')
                return False
            if not f1_chunk:
                print('Files are the same')
                return True
###############################################################################

#######################展示原项目中正则匹配式的基本原理###########################

from collections import OrderedDict #collection提供了一些容器类型，包括defaultdict和OrderDict(有序字典)
class VideoCompressionResult(object):                   #复制原项目的类定义
    def __init__(self, name):
        self.name = name
        self.ours = OrderedDict()                       #字典，且按键的插入顺序进行迭代
        self.benchmark = OrderedDict()                  #字典，且按键的插入顺序进行迭代
    def __repr__(self):                                 #返回对象的表示形式，在print的时候返回名称而非地址
        return 'VideoCompressionResult(%r)' % self.name # %r表示self.name的字符串表示形式
    
def ReMatch():              #用于展示正则匹配式的基本原理
    ###########chatGPT提供的简易demo###############
    pattern = r'(?P<first>\d+)\s(?P<second>\d+)'
    text = '123 456'
    match_result = re.match(pattern,text)
    print(match_result.groupdict())
    ###############################################

    video_files = []
    feature_bill_re = re.compile(r'^(?P<index>\d*)\s*::\s*(?P<bytes>\d+(.\d+)?)\s*\[(?P<label>.*)\]')
    output_path = 'D:\Github\losslessh264\lossless_h264_bill'
    video_result = VideoCompressionResult('video file') #实例化一个name属性为video file的VideoCompressionResult对象
    video_results = [video_result]
    line_cnt = 0
    with open(output_path, 'r') as output_file:
        for line in output_file:                        #output_file 为 bill（report）文档
            line_cnt += 1
            print(f'it is line {line_cnt}')
            if line.startswith('==='):                  #判断是否为==开头（==开头说明是分割行，包含表头信息）
                video_name = line.strip(' =\n')         #提取表头中的名称信息(去除=和空格)，作为video name
                video_files.append(video_name)          #将video name作为字符接入video_files列表
                print('###########################################')
                print(f' video name is: {video_name}   ')

                video_result = VideoCompressionResult(video_name)   #用video name创建一个VideoCompressionResult实例
                print(f' video_result is: {video_result}   ')
                video_results.append(video_result)      #将video name 的实例接入video_results列表
                continue

            m = feature_bill_re.match(line.strip())     # m表示正则表达式匹配，匹配成功则返回对象，否则是None
            if m:                                       # 判断是否是压缩信息
                label = m.groupdict()['label']          # 返回所有键为label的键值对
                print(f' label is {label} ')
                if '.' in m.groupdict()['bytes']:       # 检查捕获到的bytes的键值对中的 键 是否包含小数点
                    #将包含小数点的键值中的浮点数字符串转为整数，并作为键值，label作为键，存入benchmark字典
                    video_result.benchmark[label] = int(float(m.groupdict()['bytes']))  
                    print(f' video_result.benchmark[{label}] is {video_result.benchmark[label]}\n ')
                else:
                    #将不包含小数点的键值中的整数字符串转为整数，  并作为键值，label作为键，存入ours字典
                    video_result.ours[label] = int(m.groupdict()['bytes'])
                    print(f' video_result.ours[{label}] is {video_result.ours[label]} \n')
                continue
    print(len(video_results))   #3
    print(video_results)   
    '''[VideoCompressionResult('video file'),   #ours 和 benchmark 为空，待会儿舍去
    #VideoCompressionResult('./tibby.264'),     #ours 和 benchmark 为空，待会儿舍去
    #VideoCompressionResult('./roundtriptest/tibby.264')]   #our 和 benchmark不为空，留下'''

                                
    return [video_result for video_result in video_results      #返回值为一个含有VideoCompressionResult对象的列表
            if video_result.ours or video_result.benchmark]
video_results = ReMatch()
print(len(video_results))   #1
print(video_results)        
'''[VideoCompressionResult('./roundtriptest/tibby.264')]， #原list中唯一存活的对象'''

for item in video_results:
    print(item.benchmark)
    '''
    OrderedDict([
    ('boilerplate', 259), ('skip', 3506), ('cbpl', 9300), ('qpl', 1612), ('mb type', 4622),
    ('pred 8x8', 183), ('pred 16x16', 4579), ('pred mode', 6171), 
    ('sub mb', 333), 
    ('mv[0]', 11512), ('mv[1]', 10976), 
    ('luma dc', 2737), 
    ('chroma dc', 1999), 
    ('luma 0 eob', 45747), ('luma 0 bitmask', 2012), ('luma 0 significand', 1563), ('luma 0 sign', 4940), 
    ('luma Nth bitmask', 3417), ('luma Nth significand', 1006), ('luma Nth sign', 6908),
    ('chroma eob', 64), ('chroma sign', 11)])
    '''
    print(item.ours)
    '''
    OrderedDict([
    ('boilerplate', 847), ('skip', 3033), ('skip end', 253), ('cbpl', 7871), ('qpl', 352), ('mb type', 3714), 
    ('ref', 103), 
    ('pred 8x8', 1290), ('pred 16x16', 408), ('pred mode', 9411), 
    ('sub mb', 30), 
    ('mv[0]', 10688), ('mv[1]', 10239), 
    ('luma dc', 666), 
    ('chroma dc', 1678), 
    ('luma 0 eob', 22208), ('luma 0 bitmask', 6347), ('luma 0 exponent', 7), ('luma 0 significand', 4304), 
    ('luma 0 sign', 4351), ('luma Nth bitmask', 13469), ('luma Nth exponent', 2), ('luma Nth significand', 3774),
    ('luma Nth sign', 6678), 
    ('chroma eob', 48), ('chroma bitmask', 13), ('chroma exp', 1), ('chroma significand', 7), ('chroma sign', 12),
    ('pad byte', 34)])  
    '''
    print(item.name)    #./roundtriptest/tibby.264
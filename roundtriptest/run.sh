#!/bin/bash

set -e #遇到错误信息立刻退出

BASEDIR=`dirname "$0"`  #dirname用于获取某文件的目录，$0表示脚本文件
#此处作用在于获取脚本文件运行的根目录

#make -C "$BASEDIR/.."
pushd "$BASEDIR/.." #将目录入栈，并临时切换到指定目录
./piedpiper_make
popd                #目录出栈并切回原目录

if [ "$#" -ge 1 ]   # "$#"表示接受到的参数个数，-ge 1表示>=1
then
    FILES=()
    for f in "$@"; do   # "%@"表示所有参数
        FILES+=("$f")   # 将所有参数添加到FILES数组中
    done
else
    FILES=($BASEDIR/tibby.264)
    #FILES=($BASEDIR/tibby.264 $BASEDIR/black.264 $BASEDIR/../res/BAMQ2_JVC_C.264 $BASEDIR/../res/BA1_FT_C.264 $BASEDIR/walk.264)
    # tibby.264等文件为源文件
fi  # 表示endif

IFS=""  #Internal Field Seperator，用于确定单词边界
        #此处表示令输入行所有内容均为字段，避免文件名中的空格引起错误

REPORT=/tmp/report
rm -f $REPORT   #删除/tmp/report
for f in ${FILES[@]}; do
    rm -f /tmp/a.pip* /tmp/a.264    #删除所有a.pip开头和a.264开头的文件，包括a.pip本身
    bill=/tmp/lossless_h264_bill    #存储运行时的信息
    # tee指令用于将输出复制到文件中并且再在命令行中显示一次， -a用于将cmd内容追加到文件末尾
    echo "============== $f ================" |tee -a $bill
    echo "    ./h264dec $f /tmp/a.pip" | tee -a $bill

    #h264dec 将.264文件 解码为一连串的pip*文件(pip,pip1,...,pip69)
    ./h264dec "$f" /tmp/a.pip | tee -a $bill
    python analyze_billing.py $bill #analyze——billing.py的作用：
    
    cat $bill >> $REPORT    #将%bill的内容显示在cmd中，并且存入report
    #rm $bill                #删除bill的内容
    echo "    ./h264dec /tmp/a.pip /tmp/a.264"
    ./h264dec /tmp/a.pip /tmp/a.264
    diff /tmp/a.264 "$f"    #比较两个文件的区别，并在cmd中显示
done
echo "FULL report in $REPORT"

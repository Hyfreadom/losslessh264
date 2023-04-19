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
    FILES=($BASEDIR/tibby.264 $BASEDIR/black.264 $BASEDIR/../res/BAMQ2_JVC_C.264 $BASEDIR/../res/BA1_FT_C.264 $BASEDIR/walk.264)
fi

IFS=""

REPORT=/tmp/report
rm -f $REPORT
for f in ${FILES[@]}; do
    rm -f /tmp/a.pip* /tmp/a.264
    bill=/tmp/lossless_h264_bill
    echo "============== $f ================" |tee -a $bill
    echo "    ./h264dec $f /tmp/a.pip" | tee -a $bill
    ./h264dec "$f" /tmp/a.pip | tee -a $bill
    python analyze_billing.py $bill
    cat $bill >> $REPORT
    rm $bill
    echo "    ./h264dec /tmp/a.pip /tmp/a.264"
    ./h264dec /tmp/a.pip /tmp/a.264
    diff /tmp/a.264 "$f"
done
echo "FULL report in $REPORT"

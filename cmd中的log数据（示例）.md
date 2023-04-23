============== ./roundtriptest/tibby.264 ================	#echo的表头
    ./h264dec ./roundtriptest/tibby.264 /tmp/a.pip			#解码预告
-------------------------------------------------------		#以下为dec生成的信息
iWidth:		320												
height:		240
Frames:		94
decode time:	0.744891 sec
FPS:		126.192960 fps
-------------------------------------------------------
H264 source file name: ./roundtriptest/tibby.264..
Sequence output file name: /tmp/a.pip..
------------------------------------------------------
0 :: 847 [boilerplate]
1 :: 3033 [skip] 20783
2 :: 253 [skip end] 2810
4 :: 7871 [cbpl] 13806
6 :: 352 [qpl] 2615
7 :: 3714 [mb type] 9204
9 :: 103 [ref] 9204
10 :: 1290 [pred 8x8] 2966
11 :: 408 [pred 16x16] 2513
13 :: 9411 [pred mode] 18536
14 :: 30 [sub mb] 2692
15 :: 10688 [mv[0]] 14215
16 :: 10239 [mv[1]] 12909
17 :: 666 [luma dc] 1300
18 :: 1678 [chroma dc] 3607
19 :: 22208 [luma 0 eob] 25760
  nonzeros  0: 26.34% compressed bytes,  34494 bits encoded
  nonzeros  1: 27.36% compressed bytes,  68266 bits encoded
  nonzeros  2: 23.56% compressed bytes,  63748 bits encoded
  nonzeros  3: 12.56% compressed bytes,  21576 bits encoded
  nonzeros  4:  5.80% compressed bytes,  11094 bits encoded
  nonzeros  5:  2.55% compressed bytes,   4176 bits encoded
  nonzeros  6:  1.03% compressed bytes,   1578 bits encoded
  nonzeros  7:  0.36% compressed bytes,    522 bits encoded
  nonzeros  8:  0.25% compressed bytes,    384 bits encoded
  nonzeros  9:  0.09% compressed bytes,    136 bits encoded
  nonzeros 10:  0.04% compressed bytes,     48 bits encoded
  nonzeros 11:  0.04% compressed bytes,     56 bits encoded
  nonzeros 13:  0.00% compressed bytes,      8 bits encoded
20 :: 6347 [luma 0 bitmask] 7270
21 :: 7 [luma 0 exponent] 4
           17:  0.00% compressed bytes,      6 bits encoded
           19:  0.00% compressed bytes,      3 bits encoded
           20: 14.29% compressed bytes,      3 bits encoded
           24:  0.00% compressed bytes,      4 bits encoded
           25:  0.00% compressed bytes,      4 bits encoded
           26: 14.29% compressed bytes,      4 bits encoded
           30:  0.00% compressed bytes,      4 bits encoded
           31:  0.00% compressed bytes,      5 bits encoded
           38: 14.29% compressed bytes,      5 bits encoded
22 :: 4304 [luma 0 significand] 6307
23 :: 4351 [luma 0 sign] 5000
25 :: 13469 [luma Nth bitmask] 15090
26 :: 2 [luma Nth exponent] 0
           17:  0.00% compressed bytes,      2 bits encoded
27 :: 3774 [luma Nth significand] 7755
28 :: 6678 [luma Nth sign] 6992
29 :: 48 [chroma eob] 59
  nonzeros  0: 33.33% compressed bytes,    304 bits encoded
  nonzeros  1: 50.00% compressed bytes,    148 bits encoded
  nonzeros  2:  8.33% compressed bytes,     24 bits encoded
30 :: 13 [chroma bitmask] 17
31 :: 1 [chroma exp] 0
32 :: 7 [chroma significand] 10
33 :: 12 [chroma sign] 10
69 :: 34 [pad byte] 160
TOTAL written 111838	#ours的数据大小

#以下为benchmark（h264文件的大小）
0 :: 259.000000   [boilerplate] 
1 :: 3506.000000   [skip] 
4 :: 9300.000000   [cbpl] 
6 :: 1612.000000   [qpl] 
7 :: 4622.000000   [mb type] 
10 :: 183.000000   [pred 8x8] 
11 :: 4579.000000   [pred 16x16] 
13 :: 6171.000000   [pred mode] 
14 :: 333.000000   [sub mb] 
15 :: 11512.000000   [mv[0]] 
16 :: 10976.000000   [mv[1]] 
17 :: 2737.000000   [luma dc] 
18 :: 1999.000000   [chroma dc] 
19 :: 45747.000000   [luma 0 eob] 
20 :: 2012.000000   [luma 0 bitmask] 
22 :: 1563.000000   [luma 0 significand] 
23 :: 4940.000000   [luma 0 sign] 
25 :: 3417.000000   [luma Nth bitmask] 
27 :: 1006.000000   [luma Nth significand] 
28 :: 6908.000000   [luma Nth sign] 
29 :: 64.000000   [chroma eob] 
33 :: 11.000000   [chroma sign] 
TOTAL: 123457.000000				#benchmark即H264文件各部分的大小之和

#以下为python脚本打印的表格,本质是对上述数据的整理
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

Analysis of ./roundtriptest/tibby.264
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
#以上为python打印的表格数据，以下为解码回H.264过程中的信息
    ./h264dec /tmp/a.pip /tmp/a.264
H264 source file name: /tmp/a.pip..
Sequence output file name: /tmp/a.264..
------------------------------------------------------
-------------------------------------------------------
iWidth:		320
height:		240
Frames:		94
decode time:	0.769166 sec
FPS:		122.210290 fps
-------------------------------------------------------
TOTAL written 0
0 :: 258.000000   [boilerplate] 
1 :: 3461.000000   [skip] 
4 :: 9303.000000   [cbpl] 
6 :: 1613.000000   [qpl] 
7 :: 4624.000000   [mb type] 
10 :: 183.000000   [pred 8x8] 
11 :: 4580.000000   [pred 16x16] 
13 :: 6173.000000   [pred mode] 
14 :: 333.000000   [sub mb] 
15 :: 11516.000000   [mv[0]] 
16 :: 10980.000000   [mv[1]] 
17 :: 2738.000000   [luma dc] 
18 :: 2000.000000   [chroma dc] 
19 :: 45765.000000   [luma 0 eob] 
20 :: 2013.000000   [luma 0 bitmask] 
22 :: 1563.000000   [luma 0 significand] 
23 :: 4942.000000   [luma 0 sign] 
25 :: 3419.000000   [luma Nth bitmask] 
27 :: 1007.000000   [luma Nth significand] 
28 :: 6911.000000   [luma Nth sign] 
29 :: 64.000000   [chroma eob] 
33 :: 11.000000   [chroma sign] 
TOTAL: 123457.000000
FULL report in /tmp/report

import requests
import re
import time
import urllib
from bs4 import BeautifulSoup

#在这里输入需要选的科目和老师，科目可以重复,但科目一定不可以为空
#如果没有选老师或者没有名额的话会随机选择一位老师
#空即意味着随机
#btx->必修 ts->通识 eng->英语扩展
#目前只可以选择必修,英语扩展

preference ={
    "btx": {
        #"理论力学":"",
        #"工程热力": "",
        "计算机":"",
        #...
    },
    "ts":{

    },
    "eng":{

    },
}

user = {
    "学号": "",
    "密码": "",
}

#这里的列表的本意是来监控课余量实现自动推选课
withdrawalList = {
    
}

class Student(object):
    global preference
    host = [
        {
            'host': 'jxgl.cqu.edu.cn',
            'vs': 'dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz62hRbfKCEh4NgqUfD+QNlfnJS/3A=='
        },
        {
            'host': '202.202.1.41',
            'vs': 'dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz4b+wl1zSDOBUtpX/5BigXmPsbdDA=='
        },
        {
            'host': '202.202.1.176:8080',
            'vs': 'dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz7p2B9lkx+Yq/jf62i+iqicmZx/xg=='
        },
        {
            'host': '222.198.128.126',
            'vs': 'dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz62hRbfKCEh4NgqUfD+QNlfnJS/3A=='
        }

    ]

    CquUrl = {
        "ts": "/wsxk/stu_whszk.aspx",
        "eng": "/wsxk/stu_yytgk_bx.aspx",
        "btx": "/wsxk/stu_btx.aspx",
        #上面的基本用不到
        "checkbtx": "/wsxk/stu_btx_rpt.aspx",
        "checkeng": "/wsxk/stu_btx_rpt.aspx",
        "checkts":"/wsxk/stu_xszx_rpt.aspx",
        "submitbtx": "/wsxk/stu_btx_rpt.aspx?func=1&",
        "submiteng": "/wsxk/stu_btx_rpt.aspx?func=1&",
        "submitts":"/wsxk/stu_xszx_rpt.aspx?func=1&",
        #/wsxk/stu_btx_rpt.aspx?func=1英语扩展课程的逻辑与必修相同
        "skbj": "/wsxk/stu_xszx_skbj.aspx",
        #下面这个链接每年都会不一样不过在选课前就可以获取到
        "selspecail":"/WSXK/Private/List_WSXK_NJZY.aspx?id=0&xklb=2",
    }

    # 这是通识课的检索数据
    #SelSpeciality: 
    # sel_xq: 4
    # chk_kyme: 1
    # txt_yzm: 84gc
    # sel_lx: 4
    # kclb3: 
    # Submit: %BC%EC%CB%F7

    Tui_CquUrl={
        "eng": "/wsxk/stu_yytgkjg_bx.aspx",
        #所有的课都可以从btx里面退选
        "btx": "/wsxk/stu_txjg.aspx",
        "submit":"/wsxk/stu_txjg_rpt.aspx?func=1&"
    }

    #退课post的数据
    #chkDel13: 378207@378207-002
    #chkCount: 14
    #kclb3: %
    #id: TTT,378207@378207-002

    # 设置延迟
    def wait_time(self):
        import random
        time.sleep(1 + random.randint(0, 10) / 10)

    # 加密密码
    def __ecrpyt_passwd(self):
        import hashlib
        m = hashlib.md5()
        m.update(self.password.encode('utf-8'))
        password = m.hexdigest()
        string = self.username + password.upper()[:30] + '10611'
        n = hashlib.md5()
        n.update(string.encode('utf-8'))
        res = n.hexdigest().upper()[:30]
        return res

    # 封装get和post请求
    def get(self, url, params=None, headers=None):
        if headers == None:
            headers = self.__session.headers
        headers.update({'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"})
        res = self.__session.get(self.url + url, params=params, headers=headers)
        while res.status_code != 200:
            self.wait_time()
            res = self.__session.get(self.url + url, params=params, headers=headers)
        return res

    def post(self, url, data=None, headers=None):
        if headers == None:
            headers = self.__session.headers
        headers.update({'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"})
        res = self.__session.post(self.url + url, data=data, headers=headers)
        while res.status_code != 200:
            self.wait_time()
            res = self.__session.post(self.url + url, data=data, headers=headers)
        return res
    
    #选择老师   
    def choseTeacher(self, teacher):
        #return TeacherID,TeacherName
        #print(teacher)
        for s, t in preference[self.classes].items():
            if t!="" and t!= None:
                for schoolteacher in teacher:
                    if s in schoolteacher["subject"]:
                        if t in schoolteacher["teacher"]:
                            return {"code": schoolteacher["code"], "subject": schoolteacher["subject"], "teacher": schoolteacher["teacher"]} 
                else:
                    continue
            else:
                for schoolteacher in teacher:
                    if s in schoolteacher["subject"]:
                        import random
                        # print(teacher)
                        rd = random.randint(0, len(teacher)-1)
                        print("随机选择教师...")
                        return {"code": teacher[rd]["code"], "subject": teacher[rd]["subject"], "teacher": teacher[rd]["teacher"]}             
        print("课程未找到")
        return False
        
     #分离教师
    def splitTeachers(self, teacher):        
        flag = ""
        reteacher = []
        reValue=[]
        for index,schoolteacher in enumerate(teacher):
            flag = schoolteacher
            if (index == len(teacher) - 1):
                if (flag["name"] == schoolteacher["name"]) and (flag["subject"] == schoolteacher["subject"]):
                    reteacher.append(schoolteacher)
                    reValue.append(self.choseTeacher(reteacher))
                    print("教师选择完毕")
                    return reValue
                else:
                    reValue.append(self.choseTeacher(reteacher))
                    reteacher.clear()
            else:
                if (flag["name"] == teacher[index + 1]["name"] ) and (flag["subject"] == teacher[index + 1]["subject"] ):
                    reteacher.append(schoolteacher)
                else:
                    reteacher.append(schoolteacher)
                    reValue.append(self.choseTeacher(reteacher))
                    reteacher.clear()
                    continue
    
    # 登录
    def login(self):
        s = requests.Session()
        payload = {
            'Sel_Type': 'STU',
            '__VIEWSTATE': self.vs,
            '__VIEWSTATEGENERATOR': self.vsg,
            'aerererdsdxcxdfgfg': '',
            'efdfdfuuyyuuckjg': self.__ecrpyt_passwd(),
            'pcInfo': '',
            'txt_dsdfdfgfouyy': '',
            'txt_dsdsdsdjkjkjc': self.username,
            'txt_ysdsdsdskgf': '',
            'typeName': ''
        }
        print("正在登录……")
        res = s.post(self.url + '/_data/index_login.aspx', data=payload, headers=self.headers, proxies=self.proxies)
        # 失败重试
        if res.status_code != 200:
            print("登陆失败，正在重试，请检查账户密码及服务器可用性")
            self.wait_time()
            self.login()
        else:
                self.__session = s
                print("登陆成功")
                return True

    def checkpre(self):
        for pre in list(preference.keys()):
            for subpre in list(preference(pre).keys()):
                if subpre == "" or subpre == None:
                    print("科目名称{}非法,已删除".format(subpre))
                    preference[pre].pop(subpre)
    #更换服务器
    def antiAs(self):
        import random
        #x<=randint(x,y)<=y
        self.server=random.randint(0,3)
        self.url = "http://" + self.host[self.server]['host']
        self.vs = self.host[self.server]['vs']
        self.login()

    #在这里获取专业代号
    def get_selspecail(self):
        while True:
            re_ = self.get(Student.CquUrl["btx"])
            reg=re.compile(r"'&xn=(\d+)&xq=(\d+)'")
            if "&xn=" in re_.text:
                s = re.findall(reg, re_.text)
                # print(s)
                # print(len(s))
                if (len(s) == 1):
                    xn = s[0][0]
                    xq = s[0][1]
                    Student.CquUrl["selspecail"]+="&xn={}&xq={}".format(xn,xq)
                    print("现在是{}学年，第{}学期".format(xn, xq))
                else:
                    print("学年格式错误，重试...")
                    self.antiAs()
                    self.wait_time()
                    continue
            else:
                print("未找到学年信息，重试...")
                self.antiAs()
                self.wait_time()
                continue
            res = self.get(Student.CquUrl["selspecail"])
            if res.text.find("setTimeout(\"load_url()\",680);")== -1:
                self.selspecial = re.findall('<option value=(.*?) selected>', res.text)
                if len(self.selspecial) != 0:
                    self.selspecial=self.selspecial[0]
                print("专业代号{}".format(self.selspecial))
                break
            else:
                print("重新获取专业代号中...")
                self.antiAs()
                self.wait_time()
                continue

    #在这里进行表单提交获取数据
    def check(self):

        check_data = {
            "btx":{
            'sel_lx': '0',
            'SelSpeciality': self.selspecial,
            'Submit': '%BC%EC%CB%F7',
            # mean url decode gb2312 to 检索
            #'kclbmc': 'Nothing'
        },
            "eng" : {
            'sel_lx': '0',
            'SelSpeciality': self.selspecial,
            'Submit': '%BC%EC%CB%F7',
            'kclb3':"60",
        },
        "ts": {
            'SelSpeciality': self.selspecial,
                'sel_xq': '4',
             'chk_kyme': '1',
             'txt_yzm': '',
             'sel_lx': '4',
             'kclb3': '',
             'Submit': '%BC%EC%CB%F7',
            }
        }

        while True:
            res = self.post(Student.CquUrl['check{}'.format(self.classes)], check_data[self.classes])
            if (res.status_code != 200):
                print("请求响应状态码:{}".format(res))
                print("重新尝试提交表单中")
                self.wait_time()
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            print("Respons Check:<{}>".format(res.status_code))
            forms = soup.find_all("form")
            for form in forms:
                if "%b7%c7%d1%a1%bf%ce%ca%b1%bc%e4%a3%a1" in form.get("action"):
                    print("不在选课时间内")
                    import sys
                    sys.exit()
            return soup

    def chose(self):
        count = 0
        #rg=re.compile(r"value+\"(.*)\"")
        nameOfSubject = re.compile(r"chkKC.*")
        nameOfWindows = re.compile(r"winSKBJ.*")
        nameOfKcxf = re.compile(r"kcxf.*")
        nameOfChkSKBJ=re.compile(r"chkSKBJ\d+")
        
        soup = self.check()
        
        allWindows=soup.find_all(id=nameOfWindows)
        allSubjects = soup.find_all(id=nameOfSubject)
        allCredit=soup.find_all(id=nameOfKcxf)
        allChkSKBJ = soup.find_all(id=nameOfChkSKBJ)
        
        count = len(allSubjects)
        # 无法修改mcount变量-->赋值发生在修改前 已更正
        self.mcount = len(allSubjects)
        infos = []
        stuIndex=[]     
        
        for i in range(0, count):
            #bs4的get方法用来取得标签对象中的属性值，tag.string是tag的内容
            #python中 一个变量可以看作是一个指针，而使用中间变量给list赋值其实是赋的中间变量的地址，而不是真正想要的变量，因此要直接将变量的地址传给list
            #如temp=x->(temp->x),list.append(temp)->(list.append(&temp))
            #因此, python中的= -> =& ?
            #如a->2, b=a--->b->a,此时 a=3-->a->3, 则b->a->3
            #所以python中是传地址
            #吧

            infos.append({
                "valueSub": allSubjects[i].get("value"),
                "valueWin": allWindows[i].get("value"),
                "credit": allCredit[i].get("value"),
                "chkSKBJ":allChkSKBJ[i].get("value"),
                "id": i,  
            })

            sep='-'
            for x in range(count):
                 sep +='-'
        print(sep)
            
            # print("课程值:"+infos[i]["valueSub"])
            # print("网页值:" + infos[i]["valueWin"])
            # print("学分:" + infos[i]["credit"])
            # print("教师编码",infos[i]["chkSKBJ"])
            
        print(sep)
        print("检索结果：")
        #此处已经开始根据个人设置查询
        for sub in preference[self.classes]:
            par = re.compile((".*" + sub + ".*"))
            for info in infos:
                x = re.findall(par, info["valueSub"])
                if len(x) != 0:
                    print(x)
                    stuIndex.append(info["id"])

        print(sep)    
                    
        
        print("Info len:{}".format(len(infos)))
        print("Index find:{}".format(stuIndex))
        print()
        return {
            "stu": stuIndex,
            "info": infos,
        }       

    def query(self):
        while True:
            openWindow_data = {
            "lx": "BX",
            "id": "",
            "skbjval": "",
            }
            # link[i]->{
            #     "id": subject id,
            #     "valueSub": "subject's code",
            #     "valueWin": "link",      
            # }
            info = self.chose()
            index = info["stu"]
            link = info["info"]
    
            data = []

            for x in index:
                #查询字符串（名称/值对）
                #参数部分：从“？”开始到“#”为止之间的部分为参数部分，又称搜索部分、查询部分。
                url=("?lx={}&id={}&skbjval={}".format(openWindow_data["lx"],
                link[x]["valueWin"],
                openWindow_data["skbjval"]))
                data.append({"response":self.get(Student.CquUrl["skbj"] + url),"subID":link[x]["valueSub"],"credit":link[x]["credit"],"id":link[x]["id"]})
        
            #data->{课程response 课程id 课程学分
            # response
            # subID
            # credit
            # }

            #name=rad_0 name=rad_2 name不同的话都是必须要选一个的
        
            teacher = []
            rad = "rad_"
      
            #need subID
        
            for x in data:
                soup = BeautifulSoup(x["response"].text, "html.parser")
                cae = re.findall(r"(\[.*)\$", x["subID"])
                if len(cae) != 0:    
                    print("课程：{}|学分：{}".format(cae[0], x["credit"]))
                    x["subject"]=cae[0]
                    for x in soup.find_all(id=re.compile(rad + ".*?")):
                        #print(x.get("value"))
                        va = x.get("value")
                        #匹配的字符默认是最后一个遇到的
                        teacher.append({
                            "subject":cae[0],
                            "name": re.search(r"\@(.*)\@",va).group(1),
                            "teacher": re.search(r"\](.*)\@.*\@",va).group(1),
                            "code":re.search(r"\@.*\@(.*)",va).group(1),
                        })
                else:
                    print("解析教师id错误")
                    self.wait_time()
                    print("正在重试...")
                    continue

            print()
            return data, teacher,info["info"]
           
    def submit(self):
        #info->全部的信息
        """所有课程编码 所有课程的窗口编码 所有课程的学分 所有课程的教师编码 所有课程的id"""
        # infos.append({
        #     "valueSub": allSubjects[i].get("value"),
        #     "valueWin": allWindows[i].get("value"),
        #     "credit": allCredit[i].get("value"),
        #     "chkSKBJ":allChkSKBJ[i].get("value"),
        #     "id": i,  
        # })

        #data->个人偏好得到的数据
        """请求课程的响应文件 课程编码 课程学分 课程ID 课程名称"""
        #  data.append({
        # "response": self.get(Student.CquUrl["skbj"] + url),
        #  "subID": link[x]["valueSub"],
        #  "credit": link[x]["credit"],
        #  "id":link[x]["id"]})
        # "subject"=subjectName


        #teacher->包含着选择得到的教师的
        """教授科目 教师的组 教师的名字 教师的代码"""
        # teacher.append({
        #     "subject":cae[0],
        #     "name": re.search(r"\@(.*)\@",va).group(1),
        #     "teacher": re.search(r"\](.*)\@.*\@",va).group(1),
        #     "code":re.search(r"\@.*\@(.*)",va).group(1),
        # })

        ###需要POST的表单数据
        """
        0-mcount-1
        kcxf_:课程对应的学分
        chkSKBJ_:课程对应的教师ID;课程对应的教师ID
        chkKC_:课程编码

        sel_lx:0//这个是判断选的是通识sel_lx==2或者其他...
        sel_xq:%25
        SelSpeciality:self.selspeaciality
        kclb3: %
        chk_kyme: 0
        id:TTT,教师编码#课程编码,教师编码#课程编码,[...[...]]
        //id经过解码得到发现是需要提交的课程
        yxsjct:0
        txt_yzm: 
        """
        flags=True
        while flags:
            data, teacher, info = self.query()

            str_id = 'TTT'
            form_data = {}
            submit_data = {}

            for schoolteacher in teacher:
                print("课程：{} 教师：{}".format(schoolteacher["subject"], schoolteacher["teacher"]))
            
            #对于teacher name不同的情况要分别提交                       
            teacherid = self.splitTeachers(teacher)
            if (teacherid == False):
                self.wait_time()
                self.submit()

            #print(teacherid)
            if teacherid ==None:
                print("无老师待选")
                break
            for schoolteacher in teacherid:
                print("已选课程：{} 任课教师：{}".format(schoolteacher["subject"], schoolteacher["teacher"]))


            #提交前还需要获取已经选了的chkSKBJ
            # for i in info:
            #     print("id:{} chk:{}".format(i["id"], i["chkSKBJ"]))

            for x in range(0, self.mcount):
                #form_data["chkKC{}".format(x)]=info[x]["valueSub"]
                form_data["chkSKBJ{}".format(x)]=info[x]["chkSKBJ"]
                form_data["kcxf{}".format(x)]=info[x]["credit"]

            for da in data:
                #设置表记以多选
                flag=True
                for index, schoolteacher in enumerate(teacherid):
                    if da["subject"] == schoolteacher["subject"]:
                        if(flag):
                            form_data["chkSKBJ{}".format(da["id"])] = schoolteacher["code"]
                            flag=False
                        else:
                            form_data["chkSKBJ{}".format(da["id"])] = form_data["chkSKBJ{}".format(da["id"])] + ";"+ schoolteacher["code"]
                    
                    
            for m in data:
                for i in teacherid:
                    if m["subject"] == i["subject"]:
                        form_data["chkKC{}".format(m["id"])] = m["subID"]

            def takele(data):
                return data["id"]
            data.sort(key=takele)

            #print(data)

            for inf in data:
                str_id += ',' + form_data["chkSKBJ{}".format(inf["id"])] + '#' + inf["subID"]
        
            # str_id=str_id.encode("gb2312")

            for count in range(0, self.mcount):
                if ("chkKC{}".format(count) in form_data.keys()):
                    submit_data["kcxf{}".format(count)] = form_data["kcxf{}".format(count)]
                    submit_data["chkKC{}".format(count)] = form_data["chkKC{}".format(count)]
                    submit_data["chkSKBJ{}".format(count)] = form_data["chkSKBJ{}".format(count)]
                else:
                    submit_data["kcxf{}".format(count)] = form_data["kcxf{}".format(count)]
                    submit_data["chkSKBJ{}".format(count)] = form_data["chkSKBJ{}".format(count)]

            submit_data["mcount"]=self.mcount
            submit_data['sel_lx'] = '0'
            submit_data['sel_xq'] = '%'
            submit_data['SelSpeciality'] = self.selspecial
            submit_data['kclb3'] = '%'
            submit_data['chk_kyme'] = '0'
            submit_data['id'] =str_id
            submit_data['yxsjct'] = '0'
            submit_data['txt_yzm'] = ''

            # for x in submit_data:
            #     print(x)
        
            #print(submit_data["id"])
            #failed in last step!!!
            upload = urllib.parse.urlencode(submit_data, encoding='gb2312')

            #print("编码后"+upload)

            print("提交...")
            res = self.post(Student.CquUrl["submit{}".format(self.classes)]+upload)
            # res = self.post(Student.CquUrl["submit{}}".format(self.classes)], submit_data)
            if (res.status_code != 200):
                self.wait_time()
                continue

            resoup = BeautifulSoup(res.text, "html.parser")
            tips = resoup.find_all(text=re.compile(r"选课.*的课程"))
            for index, tip in enumerate(tips):              
                if ("选课成功" in tip):
                    print(tip)
                    subName = re.findall(r"(\[.*)/", tip) 
                    if (len(subName) == 0):
                        print("课程名称获取出现异常")
                    else:
                        print(subName[0])
                        for x in list(preference[self.classes].keys()):
                            if x in subName[0]:
                                print("删除成功课程:"+x)
                                preference[self.classes].pop(x)
                                tips.pop(index)
                else:
                    continue
            for index, tip in enumerate(tips):
                if ("选课失败" in tip):
                    print(tip)
                    if ("突破人数上限" in tip):
                        print("将会随机选择教师")
                        #选课失败的课程：[AEME21112]理论力学（Ⅲ ），原因：突破人数上限，逗号是全角符号
                        reg = re.compile(r"(\[.*)，")
                        subfaileds = re.findall(reg, tip)
                        #print(subfaileds)
                        if (len(subfaileds) != 0):
                            for subfailed in subfaileds:
                                for x in preference[self.classes]:
                                    if (x in subfailed):
                                        print("已重置教师:{}".format(preference[self.classes][x]))
                                        preference[self.classes][x] = None
                    print("正在重试...") 
                    self.wait_time()
                else:
                    flags=False        
        print("已全部完成")
        # file = open('../soup.html','w+')
        # file.write(soup.prettify())
        #value是id为winXKBJx的标签的值
        # wUrl="stu_xszx_skbj.aspx?lx=BX&id="+"value"+"&skbjval="+skbjval;

    def withdrawal(self):
        pass
    
    def __init__(self, username, password, classes="btx", server=0, proxies=None):
        self.server = server
        self.classes=classes
        self.url = "http://" + self.host[self.server]['host']
        self.vs = self.host[self.server]['vs']
        self.vsg = "CAA0A5A7"
        self.mcount=0
        self.username = username
        self.password = password
        self.proxies = proxies
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
        }
        self.login()
        self.get_selspecail()
        self.submit()

Student(user["学号"],user["密码"])

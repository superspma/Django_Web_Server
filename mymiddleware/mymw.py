from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import re


class MyMiddleware(MiddlewareMixin):
    '''自定义一个MyMiddleware类'''
    count = 0  # 此变量用于记录整个网站的访问次数

    def process_request(self, request):
        self.__class__.count += 1
        print('count=%d' % self.__class__.count)
        return None


class LimitVisit(MiddlewareMixin):
    visit_times = {}  # 键是IP地址，值是访问次数

    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        if not re.match(r'^/user/reg', request.path_info):
            return None  # (None 可省略不写)
        # 不是POST请求则放过
        if request.method != "POST":
            return
        times = self.visit_times.get('ip', 0)
        self.visit_times[ip] = times + 1  # 访问次数加1
        print(self.visit_times)
        if times > 2:
            return HttpResponse('您已经被拒绝注册！！！')

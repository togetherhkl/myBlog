# -*cding:utf-8-*-
import math
class PagInation(object):
    def __init__(self,queryset,page_size=10,page_patam="page",plus=4):
        '''
            request：请求的对象
            queryset：查询符合条件的数据（根据这个数据进行分页处理）
            page_size：每页显示数据的条数
            page_patam：url中获取页码的参数
            plus：显示分页的分页数为plux*2
        '''
        # page=request.GET.get(page_patam)
        page=page_patam
        if page is None:
            page=1
        elif page.isdecimal():
            page=int(page)
        else:
            page=1
        self.page=page
        self.page_size=page_size
        self.start_page = (page - 1) * page_size
        self.end_page = (page) * page_size
        self.queryset=queryset[self.start_page:self.end_page]
        self.page_total_count=queryset.count()
        page_count = math.ceil(self.page_total_count / (self.page_size))
        show_start_page = page - plus
        show_end_page = page + plus
        # 极大值，极小值
        if show_start_page <= 0:
            show_start_page = 1
            if page_count >= 2 * plus and page <= page_count - (2 * plus):
                show_end_page = 2 * plus + 1
            else:
                show_end_page = page_count
        if show_end_page >= page_count:
            show_end_page = page_count
            if page_count >= 2 * plus:
                show_start_page = page_count - (2 * plus)
            else:
                show_start_page = 1
        self.page_count=page_count
        self.show_start_page =show_start_page
        self.show_end_page =show_end_page
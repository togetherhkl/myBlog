$(document).ready(function () {
    BarChart()
    HandChart()
    EyeTouch()
})
var csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
function BarChart() {
    /**
     * 柱状图的显示
     * */
    var myChart = echarts.init(document.getElementById('bar-chart'));
    var option;
    option = {
        title: {
            text: '博客分类数据',
            left: 'center'
        },
        xAxis: {
            type: 'category',
            data: [],
            name: '分类',
        },
        yAxis: {
            type: 'value',
            name: '数量'
        },
        tooltip: {
            trigger: 'axis',
        },
        series: [
            {
                data: [],
                type: 'bar'
            }
        ]
    };
    $.ajax({
        url: '/blog/manage/article/data/',
        type: 'post',
        data: {'data_type': 'barchar'},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            option.xAxis.data = res.xAxis_data
            option.series[0].data = res.series_data
            myChart.setOption(option);
        }
    })
}

function HandChart() {
    /**
     * 饼图的显示
     * */
    var myChart = echarts.init(document.getElementById('hand-chart'));
    var option;
    option = {
        title: {
            text: '博客文章数据分析',
            subtext: '分类数据',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'right',
            // formatter: function (name) {
            //     return echarts.format.truncateText(name, 40, '14px Microsoft Yahei', '…');
            // },
            tooltip: {
                show: true
            }
        },
        series: [
            {
                'name': '文章数量',
                type: 'pie',
                radius: '50%',
                data: [],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
     $.ajax({
        url: '/blog/manage/article/data/',
        type: 'post',
        data: {'data_type': 'handchar'},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            option.series[0].data = res.series_data
            myChart.setOption(option);
        }
    })
}

function EyeTouch(){
    /**
     * 图标眼睛点击效果
     * */
    //页面加载值显示一个，在加载图时display必须不为none，才能加载正常，否则加载的就只是缩略图
    $('.chart').css('display','none')
    $('#bar-chart').css('display','block')
    $('.eye').click(function (){
        if($(this).parent().next().css('display')==='none'){
            $(this).removeClass('gg-eye-alt')
            $(this).addClass('gg-eye')
            $(this).parent().next().css('display','block')
        }
        else {
            $(this).removeClass('gg-eye')
            $(this).addClass('gg-eye-alt')
            $(this).parent().next().css('display','none')
        }
    })
}
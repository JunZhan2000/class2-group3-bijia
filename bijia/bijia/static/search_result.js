// /*筛选框*/
// function function1(){
//   var a =document.getElementById("taobao");
//   var b =document.getElementById("jingdong");
//   var c =document.getElementById("suning");
//   var d =document.getElementById("dangdang");
//   var e =document.getElementById("all");
//   if(a.checked===false||b.checked===false||c.checked===false||d.checked===false){
//     e.checked=false;
//   }
// }
// function function2(){
//   var a =document.getElementById("taobao");
// var b =document.getElementById("jingdong");
// var c =document.getElementById("suning");
// var d =document.getElementById("dangdang");
// var e =document.getElementById("all");
//   if(e.checked===false){
//     a.checked=false;
//     b.checked=false;
//     c.checked=false;
//     d.checked=false;
//   }
// }
//
//
//
//
// /* var search_shop = 1;//筛选电商范围
// var sort_rule = 1;//排序方式
// var min_price = $('#min_price').val();
// var max_price = $('#max_price').val(); */
// //current_page 全局变量
//
// /*
// 排序框超链接
// var sort_button = $('._dischecked');
// for (let i = 0; i <sort_button.length ; i++) {
//         var element = sort_button[i];
//         $(element).click(function(){
//             sort_rule = i+1;
//             //alert(sort_rule);
//             window.open("",'_self');
//     });
// }
// */
// $('#sort_normal').click(function(){
//   sort_rule = 1;
//   alert(sort_rule);
//   window.open(result_url,'_self');
// })
// $('#sort_high').click(function(){
//   sort_rule = 2;
//   alert(sort_rule);
//   window.open("",'_self');
// })
// $('#sort_low').click(function(){
//   sort_rule = 3;
//   alert(sort_rule);
//   window.open("",'_self');
// })
// $('#sort_num').click(function(){
//   sort_rule = 4;
//   alert(sort_rule);
//   window.open("",'_self');
// })
//
//
//
//
//
// //按钮返回顶部
// $(function(){
//     $(window).scroll(function(){  //只要窗口滚动,就触发下面代码
//
//         var scrollt = document.documentElement.scrollTop || document.body.scrollTop; //获取滚动后的高度
//
//         if( scrollt >200 ){  //判断滚动后高度超过200px,就显示
//
//             $("#gotop").fadeIn(400); //淡入
//
//         }else{
//
//             $("#gotop").stop().fadeOut(400); //如果返回或者没有超过,就淡出.必须加上stop()停止之前动画,否则会出现闪动
//
//         }
//
//     });
//     $("#gotop").click(function(){ //当点击标签的时候,使用animate在200毫秒的时间内,滚到顶部
//
//         $("html,body").animate({scrollTop:"0px"},200);
//     });
//
// });
//
// //构造动态分页按钮
// function page_ctrl(data_obj) {
//
//     //兼容 参数：翻页容器 不存在
//     //！==类型和值不都相同返回真
//       var obj_box=(data_obj.obj_box!== undefined)?data_obj.obj_box:function () {
//         return;
//       };//翻页容器dom对象,必要参数
//
//       var total_item=(data_obj.total_item!== undefined)?parseInt(data_obj.total_item):0;//数据条目总数,默认为0,组件将不加载
//
//       var per_num=(data_obj.per_num!== undefined)?parseInt(data_obj.per_num):10;//每页显示条数,默认为10条
//
//       current_page=(data_obj.current_page!== undefined)?parseInt(data_obj.current_page):1;//当前页,默认为1
//
//       var total_page=data_obj.total_page;//计算总页数,不足2页,不加载组件
//
//       if(total_page<2){
//         return;
//       }
//
//       function page_even() {
//
//         //加载数据
//         function change_content() {
//
//           //
//
//           var page_content='';//当前页内容
//
//           for(var i=0;i<per_num;i++){
//             page_content+='';
//           }
//
//           page_content+='';
//           //设置添加html
//           $('.page_content').html(page_content);
//         }
//     //创建显示内容
//         //change_content();
//
//         var inp_val=(current_page==total_page)?1:current_page+1;//跳转页数,input默认显示值（当前页）
//         var append_html='<button class="prev_page">上一页</button>';
//    for(var i = 1;i<=total_page;i++){
//        if(current_page<=6){
//            if(i == current_page){
//             append_html+='<button class="page_num current_page">'+(i)+'</button>';
//            }
//            else if(i<=7){
//             append_html+='<button class="page_num">'+(i)+'</button>';
//            }
//            else if(i == 8){
//             append_html+='<span class="page_dot"> ••• </span>';
//            }
//            else if(i >= total_page-1){
//             append_html+='<button class="page_num">'+(i)+'</button>';
//            }
//        }
//        else if(current_page>=total_page-5){
//         if(i == current_page){
//          append_html+='<button class="page_num current_page">'+(i)+'</button>';
//         }
//         else if(i>=total_page-6){
//          append_html+='<button class="page_num">'+(i)+'</button>';
//         }
//         else if(i == 3){
//          append_html+='<span class="page_dot"> ••• </span>';
//         }
//         else if(i <= 2){
//          append_html+='<button class="page_num">'+(i)+'</button>';
//         }
//     }
//     else{
//         if(i == current_page){
//             append_html+='<button class="page_num current_page">'+(i)+'</button>';
//            }
//         else if(i<=2 || i>=total_page-1 ||(i>=current_page-1&&i<=current_page+2)){
//             append_html+='<button class="page_num">'+(i)+'</button>';
//         }
//         else if(i==3 || i==total_page-2){
//             append_html+='<span class="page_dot"> ••• </span>';
//         }
//     }
//    }
//     //完成分页按钮动态样式
//         append_html+='<button class="next_page">下一页</button><span class="page_total">共 '+total_page+' 页, 到第</span><input class="input_page_num" type="text" value="'+inp_val+'"><span class="page_text">页</span><button class="to_page_num">确定</button>';
//
//         $(obj_box).children('.page_ctrl').append(append_html);
//
//         if(current_page==1){
//           //当前页为1时，前一页不可用
//           $(obj_box+' .page_ctrl .prev_page').attr('disabled','disabled').addClass('btn_dis');
//         }else{
//           $(obj_box+' .page_ctrl .prev_page').removeAttr('disabled').removeClass('btn_dis');
//         }
//
//         if(current_page==total_page){
//           $(obj_box+' .page_ctrl .next_page').attr('disabled','disabled').addClass('btn_dis');
//         }else{
//           $(obj_box+' .page_ctrl .next_page').removeAttr('disabled').removeClass('btn_dis');
//         }
//       }
//
//       page_even();
//       $(obj_box+' .page_ctrl').on('click','button',function () {
//         //取到点击对象
//         var that=$(this);
//         if(that.hasClass('prev_page')){
//           if(current_page!=1){
//             current_page--;
//             //刷新按钮样式
//             //alert(current_page);
//             window.open("",'_self');
//             //alert("www..com/search_result" + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//             that.parent('.page_ctrl').html('');
//             page_even();
//           }
//         }
//
//         else if(that.hasClass('next_page')){
//           if(current_page!=total_page){
//             current_page++;
//             //alert(current_page);
//             //alert('www..com/ + search_result' + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//             //window.open("www..com/search_result" + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//             window.open(result_url.change_page(int(current_page),'_self');
//             that.parent('.page_ctrl').html('');
//             page_even();
//           }
//         }
//     //点击页面数字跳转
//         else if(that.hasClass('page_num')&&!that.hasClass('current_page')){
//           current_page=parseInt(that.html());
//           //alert(current_page);
//           //alert('www..com/ + search_result' + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//           //window.open("www..com/search_result" + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//           window.open("",'_self');
//           that.parent('.page_ctrl').html('');
//           page_even();
//         }
//     //输入框跳转
//         else if(that.hasClass('to_page_num')){
//           var target_num = parseInt(that.siblings('.input_page_num').val());
//           if(target_num<total_page&&target_num>=0){
//             //$(obj_box+' .page_ctrl .to_page_num').removeAttr('disabled').removeClass('btn_dis');
//             current_page = target_num;
//             //alert(current_page);
//             //alert('www..com/ + search_result' + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//             //window.open("www..com/search_result" + '/' + search_baby + '/' + search_shop + '/' + sort_rule + '/'+  current_page + '/' + min_price + '/' + max_price+'');
//             window.open("",'_self');
//             that.parent('.page_ctrl').html('');
//             page_even();
//           }
//           else {
//             //$(obj_box+' .page_ctrl .to_page_num').attr('disabled','disabled').addClass('btn_dis');
//             alert("页数不存在");
//           }
//         }
//       });
//
//     }
//
//    // 'www.342342.com/' + search_result + '/' search_baby + '/' + search_shop + '/ ' + sort_rule +  current_page + '/' + mim_price + '/' + max_price;
//
// /*图片映射显示信息
// var person = $('area');
// var person_len = person.length;
// for (let i = 0; i < person_len; i++){
//     var element = person[i];
//     $(element).mouseenter(function(){
//         $('#person'+(i+1)+'').fadeIn(200);
//     });
//     $(person).mouseleave(function(){
//         $('#person'+(i+1)+'').fadeOut(100);
//     });
// } */
// var persons = $('area');
// var person = persons[0];
// $(person).mouseenter(function(){
//   $('#person1').fadeIn(200);
// });
// $(person).mouseleave(function(){
//   $('#person1').fadeOut(100);
// });
//  person = persons[1];
// $(person).mouseenter(function(){
//   $('#person2').fadeIn(200);
// });
// $(person).mouseleave(function(){
//   $('#person2').fadeOut(100);
// });
//  person = persons[2];
// $(person).mouseenter(function(){
//   $('#person3').fadeIn(200);
// });
// $(person).mouseleave(function(){
//   $('#person3').fadeOut(100);
// });
//  person = persons[3];
// $(person).mouseenter(function(){
//   $('#person4').fadeIn(200);
// });
// $(person).mouseleave(function(){
//   $('#person4').fadeOut(100);
// });
//  person = persons[4];
// $(person).mouseenter(function(){
//   $('#person5').fadeIn(200);
// });
// $(person).mouseleave(function(){
//   $('#person5').fadeOut(100);
// });
//
//
//
//
//
//
//
//
//
//
//
//
//

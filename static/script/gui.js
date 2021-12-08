var $ = mdui.$;


mdui.mutation()

var inst = new mdui.Drawer('#cs-drawer');


//深色模式
if (localStorage.getItem("cs-darkmode") == null) {
    localStorage.setItem("cs-darkmode", "false");
}
if (localStorage.getItem("cs-darkmode") == "false") {
    $("#cs-drawer-darkmode")[0].checked = false;
}
if (localStorage.getItem("cs-darkmode") == "true") {
    $("#cs-drawer-darkmode")[0].checked = true;
}

function cs_darkmode() {
    var status = $("#cs-drawer-darkmode")[0].checked
    if (status == false) {
        $("body").removeClass('mdui-theme-layout-dark');
        localStorage.setItem("cs-darkmode", "false");
    }
    if (status == true) {
        $("body").addClass('mdui-theme-layout-dark');
        localStorage.setItem("cs-darkmode", "true");
    }
}

cs_darkmode();

document.getElementById('cs-drawer-btn').addEventListener('click', function () {
    inst.toggle();
});

document.getElementById('cs-drawer-darkmode').addEventListener('click', function () {
    cs_darkmode();
});

//ajax防缓存
//$(document).ajaxStart(function (event, xhr, options) {
//    options.headers["Cache-Control"]="no-store"
//    console.log(JSON.stringify(options))
//    // xhr: XMLHttpRequest 对象
//    // options: AJAX 请求的配置参数
//});
//$(document).ajaxSetup({
//    cache: false,
//    headers: {
//        "Cache-Control": "no-cache",
//        "If-Modified-Since": "0"
//    }
//});

//ajax错误提示
$(document).ajaxError(function (event, xhr, options) {
    message = "请求出错: " + xhr.status + " " + xhr.statusText;
    mdui.snackbar({
        message: message,
        position: "right-top"
    })
});
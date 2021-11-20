var $ = mdui.$;

//注入html
$("#cs-toolbar").html(
    `
<div class="mdui-toolbar mdui-color-theme">
    <a href="javascript:;" class="mdui-btn mdui-btn-icon mdui-ripple" id="cs-drawer-btn"><i
            class="mdui-icon material-icons">menu</i></a>
    <a href="/" class="mdui-typo-headline">CloudStudy</a>
    <div class="mdui-toolbar-spacer"></div>
    <a href="/login"><button class="mdui-btn mdui-ripple mdui-hidden-xs">登录</button></a>
    <a href="/register"><button class="mdui-btn mdui-ripple mdui-hidden-xs">注册</button></a>
    <div class="cs-toolbar-account"></div>
</div>
`
);

$("#cs-drawer").html(
    `
<ul class="mdui-list">
    <li class="mdui-subheader">导航</li>
    <a href="/">
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons">home</i>
        <div class="mdui-list-item-content">首页</div>
    </li>
    </a>
    <li class="mdui-subheader">个性化</li>
    <li class="mdui-list-item mdui-ripple">
        <label class="mdui-switch">
            <input type="checkbox" id="cs-drawer-darkmode" />
            <i class="mdui-switch-icon"></i>
        </label>
        <div class="mdui-list-item-content">深色模式</div>
    </li>
    <li class="mdui-subheader mdui-hidden-sm-up">账号</li>
    <a href="/login">
    <li class="mdui-list-item mdui-ripple mdui-hidden-sm-up">
        <i class="mdui-list-item-icon mdui-icon material-icons">account_circle</i>
        <div class="mdui-list-item-content">登录</div>
    </li>
    </a>
    <a href="/register">
    <li class="mdui-list-item mdui-ripple mdui-hidden-sm-up">
        <i class="mdui-list-item-icon mdui-icon material-icons">add_circle</i>
        <div class="mdui-list-item-content">注册</div>
    </li>
    </a>
</ul>`
);

mdui.mutation()

var inst = new mdui.Drawer('#cs-drawer');
//$('title').text("CloudStudy | " + $("#cs-title").text())


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

//ajax错误提示
$(document).ajaxError(function (event, xhr, options) {
    message = "请求出错: " + xhr.status + " " + xhr.statusText;
    mdui.snackbar({
        message: message,
        position: "right-top"
    })
    // xhr: XMLHttpRequest 对象
    // options: AJAX 请求的配置参数
});
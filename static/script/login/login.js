var $ = mdui.$;
cs_checkLogin()
document.getElementById('cs-login-btn').addEventListener('click', function () {
    $("#cs-login-btn").html(`<div class="mdui-spinner mdui-center"></div>`);
    $("#cs-login-btn")[0].disabled = true;
    mdui.mutation()
    var input_email = $("#cs-login-email-input").val();
    var input_pwd = $("#cs-login-password-input").val();
    $("#cs-login-email").removeClass("mdui-textfield-invalid");
    $("#cs-login-password").removeClass("mdui-textfield-invalid");
    if (input_email == "") {
        $("#cs-login-email").addClass("mdui-textfield-invalid");
    } else {
        if (input_pwd == "") {
            $("#cs-login-password").addClass("mdui-textfield-invalid");
        } else {
            cs_login(input_email,input_pwd)
        }
    }
    $("#cs-login-btn")[0].disabled = false;
    $("#cs-login-btn").html(`登录`);
});
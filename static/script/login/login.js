var $ = mdui.$;
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
    $.ajax({
        method: 'GET',
        url: 'http://timfang.xyz:11451/api/login',
        async: false,
        headers: {
            cs_email: input_email,
            cs_password: sha512(input_pwd)
        },
        success: function (data) {
            console.log(data);
            $("#result").html(data)
        }
    });
    }}
    $("#cs-login-btn")[0].disabled = false;
    $("#cs-login-btn").html(`登录`);
});
var username;
var password;
var buttonready=true;

$(document).ready(function(){
    var lfield = $("#loginField");
    var rfield = $("#regField");

    $("#login").click(function(){
        rfield.attr("hidden","hidden");
        lfield.removeAttr("hidden");
    });
    $("#reg").click(function(){
        rfield.removeAttr("hidden");
        lfield.attr("hidden","hidden");
    });

    $("#loginGo").click(
        function(){
            if(buttonready){
            getInputs("login");
            if(checkInputs()){
                buttonready=false;
                submitInfo();
            }
        }}
    );
    $("#regGo").click(function(){
        if(buttonready){
        getInputs("reg");
        if(checkInputs()){
            buttonready=false
            submitInfo();
        }}
    });


});

function submitInfo(){
    alert("Username: "+username+"\nPassword: "+password);
    buttonready=true;
}
/*
function submitInfo(){
    var dataJson = {
        "name":username,
        "pass":password
    };
    $.ajax(
        {
            url:"",
            type:"POST",
            data:JSON.stringify(dataJson),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error:function () {alert("Communication Error, contact dev immediately");},
            success:function (data) {
                if(data==="ok") {
                    redirectSuccess();
                }else{
                    alert(data);
                    redirectFailed();
                }
            }
        }
    )
}*/

function getInputs(section) {
    username = $("#"+section+"Name").val();
    password = $("#"+section+"Pass").val();
}

//illegal character regex
var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]");
function checkInputs(){
    if(!checkUsername()){
        alert("User name should not be empty, be more than 16 characters"+
            ", or contain illegal characters");
        return false;
    }
    if(!checkPassword()){
        alert("Password should be at least 8 characters long and must not exceed 16 characters");
        return false;
    }
    return true;
}
function checkUsername(){
    if(username.length>16||username.length===0){
        return false;
    }
    return !pattern.test(username);
}
function checkPassword(){
    if(password.length>16||password.length<8){
        return false;
    }
    return true;   
}
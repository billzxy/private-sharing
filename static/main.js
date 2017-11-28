var username;
var password;
var lname="";
var fname="";
var buttonready=true;

$(document).ready(function(){
    var lfield = $("#loginField");
    var rfield = $("#regField");

    $("#login").click(function(){
        rfield.attr("hidden","hidden");
        lfield.removeAttr("hidden");
        $(".msgbox").attr("hidden","hidden");
    });
    $("#reg").click(function(){
        rfield.removeAttr("hidden");
        lfield.attr("hidden","hidden");
        $(".msgbox").attr("hidden","hidden");
    });

    $("#loginGo").click(
        function(){
            if(buttonready){
            getInputs("login");
            if(checkInputs("login")){
                buttonready=false;
                submitInfo("loginAuth");
            }
        }}
    );
    $("#regGo").click(function(){
        if(buttonready){
        getInputs("reg");
        if(checkInputs("reg")){
            buttonready=false
            submitInfo("registerAuth");
        }}
    });


});

function submitInfo(destination){
    var dataJson;
    if(destination==="registerAuth"){
        dataJson = {
            "name":username,
            "pass":password,
            "fname":fname,
            "lname":lname
        
        }
    }else{
        dataJson = {
            "name":username,
            "pass":password
        };
    }
    $.ajax(
        {
            url:destination,
            type:"POST",
            data:JSON.stringify(dataJson),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error:function () {alert("Communication Error, contact dev");},
            success:function (response) {
                var data = JSON.parse(response);
                if(data['error']) {
                    showErrorMsg(data['error']);
                    buttonready=true;
                }else{
                    window.location.replace("/feed");
                }
            }
        }
    )
}

function showErrorMsg(msg){
    $(".msgbox").removeAttr("hidden");
    $("#msg").text(msg);
}

function getInputs(section) {
    if(section==="reg"){
        fname = $("#regfname").val();
        lname = $("#reglname").val();
    }
    username = $("#"+section+"Name").val();
    password = $("#"+section+"Pass").val();
}

//illegal character regex
var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]");
function checkInputs(type){
    if(type==="reg"){     
        if(!checkRealname()){
            return false;
        }
    }
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
function checkRealname(){
    if(fname===""||lname===""){
            alert("First name or last name cannot be empty!");
            return false;   
    }else if(pattern.test(fname)||pattern.test(lname)){
        alert("Well, you really have a weird name; stop messing around and retry!");
        return false;
    }else if(fname.length>50||lname.length>50){
        alert("First name or last name cannot exceed 50 characters");
        return false;
    }
    return true;
}
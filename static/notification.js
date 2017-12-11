var notificationCount=0;
var acceptSelector;
var declineSelector;
var notiButton;

$(document).ready(function(){
    notiButton = $("#noti-button");
    username = $.cookie("username");
    renderNotificationButton();
    notiButton.click(function(){
        $(".msgbox_noti").attr("hidden","hidden");
        $(".msgbox_noti_success").attr("hidden","hidden");
        showNotification();
    });

});

function renderNotificationButton(){
    getTagNotificationCount();
}


function showNotification() {
    var agroupList = $("#notiList");
    agroupList.empty();
    $.ajax({
        data: JSON.stringify({"username":username}),
        url:"getTagMessage",
        type:"POST",
        dataType:"text",
        contentType:"application/json",
        timeout:60000,
        error: function () {alert("Retrieve notification failed!");},
        success: function (response) {
            var dataDict = JSON.parse(response);
            if(dataDict['error']) {
                showErrorMsg("_noti",dataDict["error"]);
            }else{
                var dataList = dataDict["data"];
                for(var id=0; id<dataList.length;id++){
                    var content = "<li class=\"list-group-item\" id=\"tag--"+dataList[id]['tagger']+"--"+dataList[id]['id']+"\">" +
                        dataList[id]['tagger']+" tagged you in a <a href=\""+"/content/"+dataList[id]['id']+"\">photo </a> <a class='noti-accept'>Accept </a> " +
                        "<a class='noti-decline'>Decline</a></li>";
                    agroupList.append(content);
                }
                readyNotiSelector();
            }
        }
    });
}

function readyNotiSelector(){
    acceptSelector=$("a.noti-accept");
    declineSelector=$("a.noti-decline");
    acceptSelector.click(function(){
        acceptTag($(this).parent().attr("id"));
    });
    declineSelector.click(function(){
        declineTag($(this).parent().attr("id"));
    });

}

function acceptTag(id){
    var requestData = {
            "tid":id,
            "taggee":username
    };
    $.ajax({
        url:"acceptTag",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                showErrorMsg("_noti",dataDict["error"]);
            }else{
                showSuccessMsg("_noti_success","Successfully accepted tag!");
                showNotification();
                renderNotificationButton();
            }
        }
    });
}

function declineTag(id){
    var requestData = {
            "tid":id,
            "taggee":username
    };
    $.ajax({
        url:"declineTag",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                showErrorMsg("_noti",dataDict["error"]);
            }else{
                showSuccessMsg("_noti_success","Successfully declined tag!");
                showNotification();
                renderNotificationButton();
            }
        }
    });
}

function getTagNotificationCount() {
    $.ajax({
        data: JSON.stringify({"username":username}),
        url:"getTagMsgCount",
        type:"POST",
        dataType:"text",
        contentType:"application/json",
        timeout:60000,
        error: function () {notiButton.html("Notifications("+0+")");},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                notiButton.html("Notifications("+0+")");
            }else{
                notiButton.html("Notifications("+dataDict['count']+")");
            }
        }
    });
}

function showErrorMsg(section,msg){
    var msgBox =$('#msg'+section);
    msgBox.removeClass().addClass('alert alert-primary');
    $(".msgbox"+section).removeAttr("hidden");
    msgBox.html("<strong>Oops! </strong>"+msg);
}
function showSuccessMsg(section,msg){
    var msgBox =$('#msg'+section);
    msgBox.removeClass().addClass('alert alert-success');
    $(".msgbox"+section).removeAttr("hidden");
    msgBox.html("<strong>Success! </strong>"+msg);
}

/*
function getGroupApplicationCount(){
    $.ajax({
        data: JSON.stringify({"username":username}),
        url:"getGroupMsgCount",
        type:"POST",
        dataType:"text",
        contentType:"application/json",
        timeout:60000,
        error: function () {return 0;},
        success: function (response) {
            var data = JSON.parse(response);
                if(data['error']) {
                    return 0
                }else{
                    return 0;
                }
        }
    });
}*/
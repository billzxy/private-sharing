var notificationCount=0;

$(document).ready(function(){
    username = $.cookie("username");
    getTagNotificationCount();
    getGroupApplicationCount();
    showNotification();
});

function getTagNotificationCount() {
    $.ajax({
        data: JSON.stringify({"username":username}),
        url:"getTagMsgCount",
        type:"POST",
        dataType:"text",
        contentType:"application/json",
        timeout:60000,
        error: function () {alert("Communication error");},
        success: function (response) {
            var data = JSON.parse(response);
                if(data['error']) {
                    showErrorMsg("",data['error']);//

                }else{
                    dataCount = data['count'];
                    //showPageBar();
                    getData();
                }
        }
    });
}

function getGroupApplicationCount(){
    $.ajax({
        data: JSON.stringify({"username":username}),
        url:"getGroupMsgCount",
        type:"POST",
        dataType:"text",
        contentType:"application/json",
        timeout:60000,
        error: function () {alert("Communication error");},
        success: function (response) {
            var data = JSON.parse(response);
                if(data['error']) {
                    showErrorMsg("",data['error']);//

                }else{
                    dataCount = data['count'];
                    //showPageBar();
                    getData();
                }
        }
    });
}
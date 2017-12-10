var data=[];
var username="";

$(document).ready(function(){
    username = $.cookie("username");
    getComments();
    $("#submitButton").click(function(){
        submitComment();
    });

});

function submitComment(){
    var commentText = $("#comment-text");
    var requestData = {
            "cid":cID,
            "comment_text":commentText.val(),
            "username":username
    };
    commentText.val("");

    $.ajax(
        {
            url:"postComment",
            type:"POST",
            data:JSON.stringify(requestData),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error: function (data) {alert("Communication failed! "+data);},
            success: function (result) {
                var dataDict = JSON.parse(result);
                if(dataDict["error"]){
                    showErrorMsg("_comment",dataDict["error"]);
                }else{
                    getComments();
                }
            }
        });

}

function getComments(){
    var requestData = {
            "cid":cID
    };
    $.ajax(
        {
            url:"getComments",
            type:"POST",
            data:JSON.stringify(requestData),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error: function (data) {alert("Communication failed! "+data);},
            success: function (result) {
                var dataDict = JSON.parse(result);
                if(dataDict["error"]){
                    showErrorMsg("_comment",dataDict["error"]);
                }else{
                    var feedList = $("#comment-list");
                    feedList.empty();
                    $(".msgbox_comment").attr("hidden","hidden");
                    var dataList = dataDict["data"];
                    for(var id=0; id<dataList.length;id++){
                        var content =
                        "<div class=\"card\">\n" +
                        "    <div class=\"card-body\">\n" +
                        "      <h4 class=\"card-title\">"+dataList[id]['username']+":</h4>\n" +
                        "      <p class=\"card-text\">"+dataList[id]['comment_text']+"</p>\n" +
                        "       <p>Posted On: "+dataList[id]['timest']+"</p>"+
                        "    </div>\n" +
                        "  </div>";
                        feedList.append(content);
                    }

                }
            }
        });

}

function showErrorMsg(section,msg){
    $(".msgbox"+section).removeAttr("hidden");
    $("#msg"+section).html("<strong>Oops! </strong>"+msg);
}
var username="";
var tagPeopleSelector;

$(document).ready(function(){
    username = $.cookie("username");
    getLikes();
    retrieveTags();
    getComments();

    $("#submitButton").click(function(){
        submitComment();
    });
    $("#tagButton").click(function() {
        getUntaggedUsers();
    });
    $("#likeButton").click(function() {
        likeContent();
    });
});

function getLikes(){
    var requestData = {
            "cid":cID
    };
    var likeCount = $("#likeCount");
    $.ajax({
        url:"getLikeCount",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                likeCount.html("0");
            }else{
                likeCount.html(dataDict['count']);
            }
        }
    });
}

function likeContent(){
    var requestData = {
            "username":username,
            "cid":cID
    };

    $.ajax({
        url:"likeContent",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                showErrorMsg("_like",dataDict["error"]);
            }else{
                showSuccessMsg("_like",dataDict["msg"])
            }
            getLikes();
        }
    });
}

function retrieveTags() {
    var requestData = {
            "cid":cID
    };
    var feedList = $("#tagList");
    feedList.html("");
    $.ajax(
        {
            url:"getTags",
            type:"POST",
            data:JSON.stringify(requestData),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error: function (data) {alert("Communication failed! "+data);},
            success: function (result) {
                var dataDict = JSON.parse(result);
                if(dataDict["error"]){

                }else{
                    feedList.html("");
                    var dataList = dataDict["data"];
                    for(var id=0; id<dataList.length;id++){
                        var content =dataList[id]["fname"]+" "+dataList[id]["lname"]+" ";
                        feedList.append(content);
                    }

                }
            }
        });
}

function getUntaggedUsers(){
    $("#peopleList").html("");
    var requestData = {
            "cid":cID,
            "public":isPublicContent
    };

    $.ajax({
        url:"getUntaggedUsers",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                showErrorMsg("_tag",dataDict["error"]);
            }else{
                var feedList = $("#peopleList");
                feedList.html("");
                $(".msgbox_tag").attr("hidden","hidden");
                var dataList = dataDict["data"];
                for(var id=0; id<dataList.length;id++){
                    var content = "<li data-dismiss='modal' class=\"list-group-item list-group-item-action\" " +
                            "id=\"user_"+dataList[id]["username"]+"\">"+dataList[id]["username"]+": "+dataList[id]["first_name"]
                            +" "+dataList[id]["last_name"]
                            +"</li>";
                    feedList.append(content);
                }
                readyPeopleSelector();
            }
        }
    });
}

function readyPeopleSelector(){
    tagPeopleSelector=$(".list-group-item");
    tagPeopleSelector.click(function(){
        tagPerson($(this).attr("id"));
    });
}

function tagPerson(uid){
    var requestData = {
            "taggee":uid,
            "tagger":username,
            "cid":cID
    };

    $.ajax({
        url:"tagPerson",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                showErrorMsg("_tag_after",dataDict["error"]);
            }else{
                var msgBox = $('#msg_tag_after');
                msgBox.removeClass().addClass('alert alert-success');
                $(".msgbox_tag_after").removeAttr("hidden");
                msgBox.html("<strong>Success! </strong>"+dataDict["msg"]);
            }
            getComments();
            retrieveTags();
        }
    });
}

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
                    retrieveTags();
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
                        "      <h4 class=\"card-title\">"+dataList[id]['first_name']+" "+dataList[id]['last_name']+":</h4>\n" +
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
    var msgBox =$('#msg'+section);
    msgBox.removeClass().addClass('alert alert-primary');
    $(".msgbox"+section).removeAttr("hidden");
    msgBox.html("<strong>Oops! </strong>"+msg);
}

$(document).ready(function(){
    username = $.cookie("username");
    getGroupPosts();
});

function getGroupPosts(){
    var requestData = {
            "group_name":groupName,
            "owner":owner
        };

        $.ajax(
            {
                url:"getGroupContents",
                type:"POST",
                data:JSON.stringify(requestData),
                contentType:"application/json",
                dataType:"text",
                timeout:60000,
                error: function (data) {alert("Communication failed!"+data);},
                success: function (result) {
                    var dataDict = JSON.parse(result);
                    if(dataDict["error"]){
                        showErrorMsg("",dataDict["error"]);
                    }else{
                        var feedList = $("#content_list");
                        feedList.empty();
                        var dataList = dataDict["data"];
                        for(var id=0; id<dataList.length;id++){
                            var content = "<div class='apost'><div class=\"card\" style=\"width:275px\">\n" +
                                "    <img class=\"card-img-top\" src=\"data:image/png;base64, "+dataList[id]['img']+"\" alt=\"Card image\" style=\"width:100%\">\n" +
                                "    <div class=\"card-body\">\n" +
                                "      <h4 class=\"card-title\">"+dataList[id]['caption']+"</h4>\n" +
                                "      <p class=\"card-text\">Uploaded By: "+dataList[id]['owner']+"</p>\n" +
                                "      <p class=\"card-text\">Date Uploaded: "+dataList[id]['timestamp']+"</p>\n" +
                                "      <a href=\"#\" class=\"btn btn-primary\">See Details</a>\n" +
                                "    </div>\n" +
                                "  </div></div>";
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
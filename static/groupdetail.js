var username;
var peopleListSelector;
$(document).ready(function(){
    username = $.cookie("username");
    getGroupPosts();
    if(isUserTheGroupOwner()){
        var optionArea = $("#option-area");
        optionArea.html("<button class=\"btn btn-secondary\" id=\"add_people_button\" data-toggle=\"modal\" data-target=\"#addPeopleModal\">Add People</button>"+modalWindow);
    }
    $("#add_people_button").click(function(){
        getListOfPeople();
    });
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
                                "      <a href=\"/content/"+dataList[id]['id']+"\" class=\"btn btn-primary\">See Details</a>\n" +
                                "    </div>\n" +
                                "  </div></div>";
                            feedList.append(content);
                        }

                    }
                }
            });

}

function getListOfPeople(){
    $("#peopleList").empty();
    var requestData = {
            "group_name":groupName,
            "owner":owner
    };

    $.ajax({
        url:"getNonMemberPeople",
        type:"POST",
        data:JSON.stringify(requestData),
        contentType:"application/json",
        dataType:"text",
        timeout:60000,
        error: function (data) {alert("Communication failed!"+data);},
        success: function (result) {
            var dataDict = JSON.parse(result);
            if(dataDict["error"]){
                showErrorMsg("_people",dataDict["error"]);
            }else{
                var feedList = $("#peopleList");
                feedList.empty();
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

function showErrorMsg(section,msg){
    $(".msgbox"+section).removeAttr("hidden");
    $("#msg"+section).html("<strong>Oops! </strong>"+msg);
}

function isUserTheGroupOwner() {
    return username===owner;
}

function readyPeopleSelector(){
    groupListSelector=$(".list-group-item");
    groupListSelector.click(function(){
        addPersonToGroup($(this).attr("id"));
});
}

function addPersonToGroup(uid){
    var requestData = {
            "addee":uid,
            "adder":owner,
            "group_name":groupName
    };

    $.ajax({
        url:"addPersonToGroup",
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
                $(".msgbox").removeAttr("hidden");
                $("#msg").html("<strong>Success! </strong>"+dataDict["msg"]);
            }
        }
    });
}

var modalWindow = "<div class=\"modal fade\" id=\"addPeopleModal\">\n" +
    "            <div class=\"modal-dialog\">\n" +
    "              <div class=\"modal-content\">\n" +
    "\n" +
    "                 <div class=\"modal-header\">\n" +
    "                      <h4 class=\"modal-title\">Add people:</h4>\n" +
    "                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button>\n" +
    "                 </div>\n" +
    "\n" +
    "                  <div class=\"modal-body\">\n" +
    "                      <div class=\"msgbox_people\" hidden=\"hidden\">\n" +
    "                          <div class=\"alert alert-primary\" id=\"msg_people\"></div>\n" +
    "                      </div>"+
    "                      <ul class=\"list-group\" id=\"peopleList\">\n" +
    "                      </ul>\n" +
    "                  </div>\n" +
    "\n" +
    "                  <div class=\"modal-footer\">\n" +
    "                      <button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Cancel</button>\n" +
    "                  </div>\n" +
    "\n" +
    "\n" +
    "              </div>\n" +
    "            </div>\n" +
    "      </div>"
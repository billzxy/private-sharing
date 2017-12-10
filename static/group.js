var data=[];

var username="";

$(document).ready(function(){
    username = $.cookie("username");
    getMyGroups();
    getAllGroups();
    
    $("#create").click(function(){

        var requestData = {
            "username":username,
            "groupname":$("#groupname").val(),
            "description":$("#description").val()
        };

        $.ajax(
            {
                url:"createGroup",
                type:"POST",
                data:JSON.stringify(requestData),
                contentType:"application/json",
                dataType:"text",
                timeout:60000,
                error: function (data) {alert("Communication failed!"+data);},
                success: function (result) {
                    var dataDict = JSON.parse(result);
                    if(dataDict["error"]){
                        showErrorMsg("create",dataDict["error"]);
                    }else{
                        location.reload();
                    }
                }
            });
        });
    
});


function getMyGroups(){
    var requestData = {
        "username":username
    };

    $.ajax(
        {
            url:"getMyGroups",
            type:"POST",
            data:JSON.stringify(requestData),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error: function (data) {alert("Communication failed!"+data);},
            success: function (result) {
                var dataDict = JSON.parse(result);
                if(dataDict["error"]){
                    showErrorMsg("my",dataDict["error"]);
                }else{
                    var groupList = $("#my_group_list");
                    groupList.empty();
                    var dataList = dataDict["data"];
                    for(var id=0; id<dataList.length;id++){
                        var content = "<div class='apost'><div class=\"card\" style=\"width:1000px\">\n" +
                            "    <div class=\"card-body\">\n" +
                            "      <h4 class=\"card-title\">"+dataList[id]['group_name']+"</h4>\n" +
                            "      <p class=\"card-text\">Owner: "+dataList[id]['username_creator']+"</p>\n" +
                            "      <p class=\"card-text\">Description: "+dataList[id]['description']+"</p>\n" +
                            "      <a href=\"/group/"+ dataList[id]['group_name']+"6"+dataList[id]['username_creator']+"\" class=\"btn btn-primary\">Details</a>\n" +
                            "    </div>\n" +
                            "  </div></div>";
                        groupList.append(content);
                    }

                }
            }
        });
}
function getAllGroups(){
    $.ajax(
        {
            url:"getAllGroups",
            type:"GET",
            dataType:"text",
            timeout:60000,
            error: function (data) {alert("Communication failed!"+data);},
            success: function (result) {
                var dataDict = JSON.parse(result);
                if(dataDict["error"]){
                    showErrorMsg("all",dataDict["error"]);
                }else{
                    var agroupList = $("#all_group_list");
                    agroupList.empty();
                    var dataList = dataDict["data"];
                    for(var id=0; id<dataList.length;id++){
                        var content = "<div class='apost'><div class=\"card\" style=\"width:1000px\">\n" +
                            "    <div class=\"card-body\">\n" +
                            "      <h4 class=\"card-title\">"+dataList[id]['group_name']+"</h4>\n" +
                            "      <p class=\"card-text\">Owner: "+dataList[id]['username']+"</p>\n" +
                            "      <p class=\"card-text\">Description: "+dataList[id]['description']+"</p>\n" +
                            "      <a href=\"#\" class=\"btn btn-primary\">Apply</a>\n" +
                            "    </div>\n" +
                            "  </div></div>";
                        agroupList.append(content);
                    }

                }
            }
        });
}

function showErrorMsg(type,msg){
    $(".msgbox_"+type).removeAttr("hidden");
    $("#msg_"+type).html("<strong>Oops! </strong>"+msg);
}
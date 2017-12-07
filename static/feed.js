var data=[];

var dataCount;
var showMax=10;
var onPage=1;
var pageCount;
var isPageBarReady=false;
var maxSearchResult=10;
var username="";


$(document).ready(function(){
    username = $.cookie("username");
    $.ajax({
        data: JSON.stringify({"username":username}),
        url:"getPostCount",
        type:"POST",
        dataType:"text",
        contentType:"application/json",
        timeout:60000,
        error: function () {alert("Communication error");},
        success: function (response) {
            var data = JSON.parse(response);
                if(data['error']) {
                    showErrorMsg(data['error']);//

                }else{
                    dataCount = data['count'];
                    //showPageBar();
                    getData();
                }
        }
    });

});


function getData(){
    var pageRequest = {
        "page": onPage,
        "max":showMax,
        "username":username
    };

    $.ajax(
        {
            url:"getPosts",
            type:"POST",
            data:JSON.stringify(pageRequest),
            contentType:"application/json",
            dataType:"text",
            timeout:60000,
            error: function (data) {alert("Communication failed!"+data);},
            success: function (result) {
                var dataDict = JSON.parse(result);
                if(dataDict["error"]){
                    showErrorMsg(dataDict["error"]);
                }else{
                    var feedList = $("#feed_list");
                    feedList.empty();
                    var dataList = dataDict["data"];
                    for(var id=0; id<dataList.length;id++){
                        var tr = "<tr>" +
                            "<td>Content name:"+dataList[id]['content_name']+"</td>" +
                            "<td><img src=\"data:image/png;base64, "+dataList[id]['img']+"\" /></td>"+
                            "</tr>";


                        feedList.append(tr);
                    }

                }
            }
        });
}

function showErrorMsg(msg){
    $(".msgbox").removeAttr("hidden");
    $("#msg").text(msg);
}

function showPageBar(){
    pageCount = Math.ceil(dataCount/showMax);
    for(var i=1;i<=pageCount;i++){
        var pageN='<li class=""><a href="#" id="'+i+'">'+" "+i+" "+'</a></li>';
        $('#page').append(pageN);
    }
}

function stripBase64Img(imgString){

}

function getPosts(){

}
$(function(){

	$("#login").on("click",function(){
	
		var username = $("#username").val()
		var password = $("#password").val()

		$.ajax({
                        type : "post",
                        url : "/login",
                        data: {"username":username,"password":password},
                        success:function(msg){
                                if (msg == 'ok'){
					window.location = "index"
                                }
                                else{

					$("#alert").text("用户名或密码错误")	
                                }
                        }
                });
	});

});

$(function(){

	$("#repeat-password").bind("input propertychange",function(){
		
		var password = $("#password").val()

		if (password == $(this).val())
		{
			$(this).css("background-color","white")
			$("#register").removeAttr("disabled")
		}
		else
		{
			$("#register").attr("disabled")
			$(this).css("background-color","red")
		}
		
	});

	$("#register").on("click",function(){
	
		var username = $("#username").val()
		var password = $("#password").val()

		$.ajax({
                        type : "post",
                        url : "/register",
                        data: {"username":username,"password":password},
                        success:function(msg){
                                if (msg == 'ok'){
					window.location = "index"
                                }
                                else{
					alert(msg)
                                }
                        }
                });
	});

});

$(function(){

	$('div[name=old_answer]').each(function(){

		if($(this).children().is('img')){
			var index_id = $(this).attr('id');		
			var input_id = index_id.substring(5,6);
			$("#" + input_id).remove();
		}
	});

	$('button[name=mark_btn]').on('click', function () {

		var mark = $(this).attr("id")
		var oldid = $("div#q_old_id").text()
		var newid = $("div#q_new_id").text()
		var this_btn = $(this)

		$.ajax({
			type : "post",
			url : "/mark",
			data:{"mark" : mark,"oldid" : oldid,"newid" : newid},
			success:function(msg){
				if (msg == 'ok'){

    					this_btn.button('loading');
				}
				else{
					this_btn.button('reset');
				}
			}
		});
	});

	$('button#add_mark').on('click',function() {
		
		var name = $("input#mark_data").val()
		var oldid = $("div#q_old_id").text()

		$.ajax({
			type : "post",
			url : "/addmark",
			data:{"name" : name,"oldid" : oldid},
			success:function(msg){
				if (msg == 'ok'){
					alert('添加成功');
				}
				else{
					alert('添加失败');
				}
			}
		});

	});
	
	$('button#pass').on('click',function() {
		var this_btn = $(this);
		var oldid = $("div#q_old_id").text()
		var newid = $("div#q_new_id").text()

		$.ajax({
			type : "post",
			url : "/verify",
			data: {"oldid":oldid,"newid":newid,"verify":0},
			success:function(msg){
				if (msg == 'ok'){
					this_btn.button("loading");
					$("#no").button("loading");
				}
				else{
					this_btn.button("reset");
					$("#no").button("reset");

				}
			}
		});

	});

	$('button#no').on('click',function() {
		var this_btn = $(this);
		var oldid = $("div#q_old_id").text()
		var newid = $("div#q_new_id").text()

		$.ajax({
			type : "post",
			url : "/verify",
			data: {"oldid":oldid,"newid":newid,"verify":1},
			success:function(msg){
				if (msg == 'ok'){
					this_btn.button("loading");
					$("#pass").button("loading");
				}
				else{
					this_btn.button("reset");
					$("#no").button("reset");

				}
			}
		});

	});

	$("input[name=new_answer]").focus(function(){
		$(this).css("background","white");
	});


	$('button#submit_answer').on('click',function() {
		var this_btn = $(this);
		var oldid = $("div#q_old_id").text()
		var new_answer = ""
		var flag = true

		$("input[name=new_answer]").each(function(){
			var index = $(this).attr("id");
			new_answer += index + ",";
			var v = $(this).val();
			new_answer += v + "|";
			/*
			if (!v){
				$(this).css("background","#FFEBCD");
				flag = false;
				return false;
			}
			*/
		});
		
		if(flag){

			$.ajax({
					type : "post",
					url : "/submit_answer",
					data: {"oldid":oldid,"new_answer":new_answer},
					success:function(msg){
						if (msg == 'ok'){
							this_btn.button("loading");
						}
						else{
							this_btn.button("reset");
						}
					}
			});
		}
	});

});

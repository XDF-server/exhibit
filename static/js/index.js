$(function(){
	
	function clear_last_input()
	{
		$("#search-data").val("");
		$("input#search-data").css("background","#fff");
	}

	function check_input()
	{
		var search_data = $("#search-data").val();
		
		if(0 == search_data.length)
		{
			return -1;
		}
		
		return 0;
	}

	function input_warning()
	{
		$("input#search-data").css("background","#FFEBCD");	
	}

	$('#background').height($(window).height());
	$('#background').width($(window).width());


	$("#search-data").focus(function(){
		clear_last_input();
	});

	$("#search-btn").click(function(){

		if(0 == check_input())
		{
			data = $("#search-data").val()
			$("#search_data").attr("value",data);
			$("#search_type").attr("value","1");
			$("#search-form").submit();
			clear_last_input()
		}
		else
		{
			clear_last_input();
			input_warning();
		}
	});

	$("#single_choice").click(function(){
			$("#search_type").attr("value","2");
			$("#search_data").attr("value","1")
			$("#search-form").submit();
	});
/*
	$("#cp-id-search").click(function(){
		if(0 == check_input())
		{	
			$("#search_type").attr("value","3");
			$("form").submit();
			clear_last_input()
		}
		else
		{
			clear_last_input();
			input_warning();
		}
	});
	
	$("#voucher-id-search").click(function(){
		if(0 == check_input())
		{	
			$("#search_type").attr("value","4");
			$("form").submit();
			clear_last_input()
		}
		else
		{
			clear_last_input();
			input_warning();
		}
	});
*/
});

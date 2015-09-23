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

	$("a[name=type]").click(function(){
		$("#search_type").attr("value","2");
		var type = $(this).text();
		$("#search_data").attr("value",type)
		$("#search-form").submit();
	});

	$("a[name=subject]").click(function(){
		$("#search_type").attr("value","3");
		var subject = $(this).text();
		$("#search_data").attr("value",subject)
		$("#search-form").submit();
	});

	$("#paper-search").click(function(){

		if(0 == check_input())
		{
			data = $("#search-data").val()
			$("#search_data").attr("value",data);
			$("#search_type").attr("value","4");
			$("#search-form").submit();
			clear_last_input()
		}
		else
		{
			clear_last_input();
			input_warning();
		}
	});


/*
	$("#single_choice").click(function(){
			$("#search_type").attr("value","2");
			$("#search_data").attr("value","1")
			$("#search-form").submit();
	});

	$("#gap_filling").click(function(){
			$("#search_type").attr("value","2");
			$("#search_data").attr("value","2")
			$("#search-form").submit();
	});
	
 	$("#true_or_false").click(function(){
			$("#search_type").attr("value","2");
			$("#search_data").attr("value","3")
			$("#search-form").submit();
	});

	$("#short_answer").click(function(){
			$("#search_type").attr("value","2");
			$("#search_data").attr("value","4")
			$("#search-form").submit();
	});

	$("#math").click(function(){
			$("#search_type").attr("value","3");
			$("#search_data").attr("value","1")
			$("#search-form").submit();
	});

	$("#chinese").click(function(){
			$("#search_type").attr("value","3");
			$("#search_data").attr("value","2")
			$("#search-form").submit();
	});
	
 	$("#english").click(function(){
			$("#search_type").attr("value","3");
			$("#search_data").attr("value","3")
			$("#search-form").submit();
	});

	$("#history").click(function(){
			$("#search_type").attr("value","3");
			$("#search_data").attr("value","4")
			$("#search-form").submit();
	});
*/
});

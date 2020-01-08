function start() {
    $.ajax({
	    url: '/start',
	    success: function(data){
	    	alert("Libfuse running!");
	    },
	    error: function(error){
		    console.log(error);
	    }
    });
}

function stop() {
    $.ajax({
	    url: '/stop',
	    success: function(data){
	    	alert("Libfuse unmounted!");
	    },
	    error: function(error){
		    console.log(error);
	    }
    });
}

function terminal() {
    $.ajax({
	    url: '/terminal',
	    success: function(data){
	    	
	    },
	    error: function(error){
		    console.log(error);
	    }
    });
}

function folder() {
    $.ajax({
	    url: '/folder',
	    success: function(data){
	    	
	    },
	    error: function(error){
		    console.log(error);
	    }
    });
}
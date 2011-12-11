$(document).ready(function(){
    $(function() {
		var cache = {},
			lastXhr;
		$( "#player_search" ).autocomplete({
			minLength: 1,
			source: function( request, response ) {
				var term = request.term;
				if ( term in cache ) {
					response( cache[ term ] );
					return;
				}

				lastXhr = $.getJSON( "/player_search/", request, function( data, status, xhr ) {
					cache[ term ] = data;
					if ( xhr === lastXhr ) {
						response( data );
					}
				});
			},
                        select: function(event, ui){
                            $("#player_search_id").val(ui.item.id);
                        }
		});
	});
});
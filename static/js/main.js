$.isSubstring = function(haystack, needle) {
	return haystack.indexOf(needle) !== -1;
};

gup = function( name ) {
	name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
	var regexS = "[\\?&]"+name+"=([^&#]*)";
	var regex = new RegExp( regexS );
	var results = regex.exec( window.location.href );
	if( results == null ) {
		return "";
	} else {
		return results[1];
	}
}

playAlbum = function( album ) {
	$.ajax({
		url: "/playalbum?album="+album,
		success: function(data) {
			console.log( data );
		}
	});
}

playSong = function( song ) {
	$.ajax({
		url: "/playsong?song="+escape(song),
		success: function(data) {
			console.log( data );
		}
	});
}

$( document ).ready( function() {
	$("#albums li a").each( function() {
		$(this).click( function(event) {
			event.preventDefault();
			//console.log($(this).attr("id"));
			playAlbum( $(this).attr("id"));
		})
	});

	$(".songs li a").each( function() {
		$(this).click( function(event) {
			event.preventDefault();
			//console.log($(this).attr("id"));
			playSong( $(this).attr("id") );
		})
	});

	$(".more-less").each( function() {
		$(this).siblings('ul').toggle()
		$(this).click( function(event) {
			event.preventDefault();
			$(this).siblings('ul').toggle();
			if( $(this).text() == "(collapse)" ) {
				$(this).text("(expand)");
			} else {
				$(this).text("(collapse)");
			}
		})
	});
});
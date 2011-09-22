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

$( document ).ready( function() {
	$("#albums li a").each( function() {
		$(this).click( function(event) {
			event.preventDefault();
			console.log($(this).attr("id"));
		})
	});
});
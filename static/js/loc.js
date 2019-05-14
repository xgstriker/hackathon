$(document).ready(function() {

		navigator.geolocation.getCurrentPosition(function(position){
			$("#lat").val(position.coords.latitude);
			$("#lng").val(position.coords.longitude);
			$(".row").submit();
		});

});
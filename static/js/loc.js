$(document).ready(function() {

  if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position){
			$("#lat").val(position.coords.latitude);
			$("#lng").val(position.coords.longitude);
			$(".row").submit();
		}); } else {
			$(".row").submit();
		}

});
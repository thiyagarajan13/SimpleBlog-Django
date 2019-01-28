function likeProduct(){
	$('a[id^=itemLike]').on("click", function(e) { // catch the form's submit event
		e.preventDefault();
		var aId = $(this).attr('id');
		var itemID = aId.substring(8);
		$.ajax({
			url:'/product/'+itemID+'/',
			success: function(data) { // on success..
				var rating_status = jQuery.parseJSON(data);
				if (rating_status.Success == "True") {
				$('a').find('#heart-icon' + itemID).removeClass('fa-heart-o text-not-liked').addClass('fa-heart text-liked');
				$('#like-count' + itemID).html(rating_status.count);
				} else if (rating_status.Removed == "True") {
				$('a').find('#heart-icon' + itemID).removeClass('fa-heart text-liked').addClass('fa-heart-o text-not-liked');
				$('#like-count' + itemID).html(rating_status.count);
				}
			},/* end of success */
			error: function(data) {
				setTimeout(function() {$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});}, 1000);
			}/*  end of error */
		});/* end of ajax */
	});/* end of onclick*/
};/* end of likeProduct()*/
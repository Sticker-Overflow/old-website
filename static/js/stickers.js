$(document).ready(function(){
	
	$("#search-icon").hide();
	var config = {
		apiKey: "AIzaSyC5x_SZTHN8UcVYw2aQioJE2fOqXdE3Mcg",
		authDomain: "stickeroverflow-1d318.firebaseapp.com",
		databaseURL: "https://stickeroverflow-1d318.firebaseio.com",
		projectId: "stickeroverflow-1d318",
		storageBucket: "stickeroverflow-1d318.appspot.com",
		messagingSenderId: "951520957692"
	};
	firebase.initializeApp(config);

	  // Initialize Cloud Firestore through Firebase
	var db = firebase.firestore();
	var storage = firebase.storage();

	var cursor = null;

	db.collection("stickers").orderBy("dateAdded", "desc").orderBy("name").limit(30).get().then((querySnapshot) => {
		querySnapshot.forEach((doc) => {
			cursor = doc;

			storage.ref("stickers/" + doc.data().id + "/" + doc.data().id + ".png").getDownloadURL().then(function(url) {
				$("#putStickersHere").append(createStickerCard(doc.data().id, url));
			});
		});
	});

	$("#loadMoreButton").click(function() {
		db.collection("stickers").orderBy("dateAdded", "desc").orderBy("name").limit(30).startAfter(cursor).get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				cursor = doc;
				storage.ref("stickers/" + doc.data().id + "/" + doc.data().id + ".png").getDownloadURL().then(function(url) {
					$("#putStickersHere").append(createStickerCard(doc.data().id, url));
				});
			});
		});
	});

});


function createStickerCard(id, image) {
	var html = '<div class="col s6 m3 l2">' + 
			'<div id="' + id + '" class="sticker hoverable">' + 
				'<a href="/stickers/' + id + '"><img class="sticker-image" src="' + image + '"></a>' + 
			'</div>' +
		'</div>'
	return html;
}

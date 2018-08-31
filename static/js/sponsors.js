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

	var cursor = null;

	db.collection("sponsors").orderBy("name").orderBy("description").limit(20).get().then((querySnapshot) => {
		querySnapshot.forEach((doc) => {
			cursor = doc;
			$("#putSponsorsHere").append(createSponsorCard(doc.data().id, doc.data().name, doc.data().logoURL, doc.data().location));
		});
	});

	$("#loadMoreButton").click(function() {
		db.collection("sponsors").orderBy("name").orderBy("description").limit(20).startAfter(cursor).get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				cursor = doc;
				$("#putSponsorsHere").append(createSponsorCard(doc.data().id, doc.data().name, doc.data().logoURL, doc.data().location));
			});
		});
	});

});


function createSponsorCard(id, name, logo, location) {
	var html = '<div class="col s12 m6 l3">' +
                        '<a href="/sponsors/' + id + '">' +
                                '<div id="' + id + '" class="card-panel grey lighten-5 z-depth-1 hoverable">' +
                                        '<div class="row valign-wrapper">' +
                                                '<div class="col s3">' +
                                                        '<div class="logo-container valign-wrapper">' +
                                                                '<img class="sponsors-logo clickable" src="' + logo + '" alt="' + name + '">' +
                                                        '</div>' +
                                                '</div>' +
                                                '<div class="col s9">' +
                                                        '<span class="black-text">' + name + '</span>' +
                                                        '<br>' +
                                                        '<span class="black-text">' + location + '</span>' +
                                                '</div>' +
                                        '</div>' +
                                '</div>' +
                        '</a>' +
                '</div>'
        return html;
}

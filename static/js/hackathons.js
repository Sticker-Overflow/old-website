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

	db.collection("hackathons").orderBy("date", "desc").orderBy("name").limit(18).get().then((querySnapshot) => {
		querySnapshot.forEach((doc) => {
			cursor = doc;
			$("#putHackathonsHere").append(createHackathonCard(doc.data().id, doc.data().name, doc.data().splashURL, doc.data().logoURL, doc.data().location, doc.data().dateString));
		});
	});

	$("#loadMoreButton").click(function() {
		db.collection("hackathons").orderBy("date", "desc").orderBy("name").limit(18).startAfter(cursor).get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				cursor = doc;
				$("#putHackathonsHere").append(createHackathonCard(doc.data().id, doc.data().name, doc.data().splashURL, doc.data().logoURL, doc.data().location, doc.data().dateString));
			});
		});
	});

});


function createHackathonCard(id, name, splash, logo, location, date) {
	var html = '<div class="col s12 m4 l2">' + 
			'<a href="/hackathons/' + id + '">' + 		
				'<div id="' + id + '" class="card hoverable">' + 
					'<div class="card-image">' + 
						'<img class="hackathon-splash clickable" src="' + splash + '">' +
					'</div>' + 
						'<img class="hackathon-logo z-depth-5" src="' + logo + '">' + 
					'<div class="card-content hackathon-details">' + 
						'<p class="center-align hackathon-name truncate">' + name + '</p>' +
						'<p class="center-align">' + location + '</p>' +
						'<p class="center-align">' + date + '</p>' +
					'</div>' +
				'</div>' +
			'</a>' +
		'</div>';
	return html;
}

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

	db.collection("users").orderBy("name").limit(15).get().then((querySnapshot) => {
		querySnapshot.forEach((doc) => {
			cursor = doc;
			if(doc.data().uid !== $.cookie("jUid")) {
				$("#putUsersHere").append(createUserCard(doc.data().uid, doc.data().photoUrl, doc.data().name));
			}
		});
	});

	$("#loadMoreButton").click(function() {
		db.collection("users").orderBy("name").limit(15).startAfter(cursor).get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				cursor = doc;
				if(doc.data().uid !== $.cookie("jUid")) {
					$("#putUsersHere").append(createUserCard(doc.data().uid, doc.data().photoUrl, doc.data().name));
				}
			});
		});
	});

});

function createUserCard(id, image, userName) {
	var html = 
		'<div class="col s12 m8 offset-m2 l6 offset-l3">' + 
			'<a href="/users/' + id + '">' + 
				'<div id="' + id + '" class="card-panel grey lighten-5 z-depth-1">' + 
					'<div class="row remove-bottom-margin valign-wrapper">' + 
						'<div class="col s3">' + 
							'<img src="' + image + '" alt="" class="circle responsive-img">' + 
						'</div>' + 
						'<div class="col s9">' + 
							'<span class="black-text users-name">' + userName + '</span>' + 
						'</div>' + 
					'</div>' + 
				'</div>' + 
			'</a>' + 
		'</div>';
	return html;
}



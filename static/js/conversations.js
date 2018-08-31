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

	db.collection("users").doc($.cookie("jUid")).collection("conversations").orderBy("lastModified", "desc").orderBy("otherUserId").limit(8).get().then((querySnapshot) => {
		querySnapshot.forEach((doc) => {
			cursor = doc;
			db.collection("users").doc(doc.data().otherUserId).get().then((userDoc) => {
				$("#putConversationsHere").append(createConversationCard(doc.data().id, doc.data().latestMessage, userDoc.data().photoUrl, userDoc.data().name, doc.data().lastModified, doc.data().numberOfUnreadMessages));
			});
		});
	});

	$("#loadMoreButton").click(function() {
		db.collection("users").doc($.cookie("jUid")).collection("conversations").orderBy("lastModified", "desc").orderBy("otherUserId").limit(8).startAfter(cursor).get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				cursor = doc;
				db.collection("users").doc(doc.data().otherUserId).get().then((userDoc) => {
					$("#putConversationsHere").append(createConversationCard(doc.data().id, doc.data().latestMessage, userDoc.data().photoUrl, userDoc.data().name, doc.data().lastModified, doc.data().numberOfUnreadMessages));
				});
			});
		});
	});
});

// TODO
function createConversationCard(id, latestMessage, otherUserPhoto, otherUserName, lastModified, numberOfUnreadMessages) {
	var html = 
		'<a href="/conversations/' + id + '">' + 
			'<li id="' + id + '" class="collection-item avatar">' + 
				'<img src="' + otherUserPhoto + '" alt="' + otherUserName + '" class="circle">' + 
				'<span class="title">' + otherUserName + '</span>';

		if(numberOfUnreadMessages > 0) {
			html += '<span class="new badge">' + numberOfUnreadMessages + '</span>';
		}

		var lastModifiedDate = new Date(lastModified);

		html += '<p>' + latestMessage + '<br>' + lastModifiedDate.customFormat('#hh#:#mm# #ampm#') +
			'</p>'
		'</li></a>';

	return html;
}

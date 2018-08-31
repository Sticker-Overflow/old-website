$(document).ready(function(){
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

	db.collection("users").doc($.cookie("jUid")).collection("conversations").doc(window.location.pathname).collection("messages").orderBy("createdAt", "desc").orderBy("text").get().then((querySnapshot) => {
		querySnapshot.forEach((doc) => {
			if(userDoc.data().senderId !== $.cookie("cUid")) {
				db.collection("users").doc(userDoc.data().senderId).get().then((otherUserDoc) => {
					$("#putConversationsHere").append(createMessage(doc.data().id, doc.data().text, userDoc.data().senderId, userDoc.data().name, doc.data().lastModified, doc.data().numberOfUnreadMessages));
				});
			} else {
				$("#putConversationsHere").append(createMessage(doc.data().id, doc.data().text, null, userDoc.data().name, doc.data().lastModified, doc.data().numberOfUnreadMessages));
			}
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

		html += '<p>' + latestMessage + '<br>' + lastModified + 
			'</p>'
		'</li></a>';
	return html;
}

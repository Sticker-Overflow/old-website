$(document).ready(function(){
	$("#search-icon").hide();
	$("#upload-form").submit(function(e) {
		e.preventDefault();
		var file = $("#file-select")[0].files[0];
		var formData = new FormData();
		if(!file.type.match('image.*')) {
			return;
		}
		formData.append("picture", file, file.name);
		var xhr = new XMLHttpRequest();
		xhr.open("POST", "/web_upload", true);
		xhr.onreadystatechange = function() {
			if(xhr.readyState === 4 && xhr.status === 200) {
				var response = JSON.parse(xhr.response);
			
				var results = response["Result"].split(",");
				
				var tempDict = {};
				
				results.forEach(function(result) {
					var id = result.split(":")[0];
					var percentage = result.split(":")[1];
					tempDict[id] = percentage;
				});

				var res = Object.keys(tempDict).map(function(key) {
					return [key, tempDict[key]];
				});

				res.sort(function(first, second) {
					return parseInt(first[1]) - parseInt(second[1]);
				});

				res.forEach(function(r) {
					$("#image-list").append("<div id='" + r[0] + "' class='col s12'></div>");
					createStickerCard(r[0], r[1]);
				});
			}
		};
		xhr.send(formData);

	});

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

	var db = firebase.firestore();
	var storage = firebase.storage();
		
	function createStickerCard(id, percentage) {
		db.collection("stickers").doc(id).get().then(function(doc) {
			storage.ref("stickers/" + id + "/" + id + ".png").getDownloadURL().then(function(url) {
				var html = "<a href='/stickers/" + id + "'>" + 
						"<div class='card-panel grey lighten-5 z-depth-2'>" + 
							"<div class='row valign-wrapper'>" + 
								"<div class='col s4'>" + 
									"<img src='" + url + "' alt='" + doc.data().name + "' class='responsive-img'>" + 
								"</div>" + 
							"<div class='col s8'>" + 
								"<span class='black-text'>" + 
									(percentage * 100).toFixed(2) + "% match"
								"</span>" + 
							"</div>" + 
						"</div>" + 
					"</a>";
				$("#" + id).append(html);
			});
		});		
	}
});

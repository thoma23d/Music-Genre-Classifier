// brew install node
// npm install -g bower
// bower install spotify-web-api-js

// npm install -g browserify
// npm install -S spotify-web-api-js
// node spotify.js

window.onload = function(){
  console.log(data);

	var tryAgain = document.getElementById('tryAgain');
  var audio = document.getElementById('mp3');
	var noAudio = document.getElementById('noAudio');

	if (data.preview_url === null){
		audio.style.display = "none";
		noAudio.style.display = "block";	
	}
	else if (data.preview_url !== null){
		audio.style.display = "block";
		noAudio.style.display = "none";	
	}
  
  var header = document.getElementById('header');
  var classifiedText = document.getElementById('classified');
  var searched = document.getElementsByClassName('searched');

  if (data.genre == 'Pop') {
    header.style.backgroundColor = "#FE53BB";
    searched[0].style.color = "#FE53BB";
    searched[1].style.color = "#FE53BB";
    searched[2].style.color = "#FE53BB";
	}
	if (data.genre == 'Rock') {
  	header.style.backgroundColor = "#6e0dd0";
    searched[0].style.color = "#6e0dd0";
    searched[1].style.color = "#6e0dd0";
    searched[2].style.color = "#6e0dd0";
  }
  if (data.genre == 'Latin') {	
  	header.style.backgroundColor = "#FC6E22";
    searched[0].style.color = "#FC6E22";
    searched[1].style.color = "#FC6E22";
    searched[2].style.color = "#FC6E22";
  }
  if (data.genre == 'Rap') {	
  	header.style.backgroundColor = "#ce1127";
    searched[0].style.color = "#ce1127";
    searched[1].style.color = "#ce1127";
    searched[2].style.color = "#ce1127";
  }
  if (data.genre == 'Edm') {
  	header.style.backgroundColor = "dimgrey";	
    searched[0].style.color = "dimgrey";
    searched[1].style.color = "dimgrey";
    searched[2].style.color = "dimgrey";
 	}
 	if (data.genre == 'R&B' ) {	
 		header.style.backgroundColor = "#00218A";
    searched[0].style.color = "#00218A";
    searched[1].style.color = "#00218A";
    searched[2].style.color = "#00218A";
  }
  if (data.genre == 'Country') {	
  	header.style.backgroundColor = "olive";	
    searched[0].style.color = "olive";
    searched[1].style.color = "olive";
    searched[2].style.color = "olive";
  }
};

function displayPdf(){
  var graph = document.getElementById('proba_graph');
  graph.style.visibility = 'visible';
};

function hidePdf(){
  var graph = document.getElementById('proba_graph');
  graph.style.visibility = 'hidden';
};








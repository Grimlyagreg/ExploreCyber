const postsElem = document.getElementById("posts");
var userToken = null;
var userName = null;

function login(username, password) {
	var token = sendRequest("/login", {username: username, password: password});
	if(token !== "FAIL") {
		userToken = token;
		userName = username;
		updateScreen();
	} else {
		alert("Incorrect username or password.");
	}
}

function signUp(username, password) {
	var token = sendRequest("/signup", {username: username, password: password});
	if(token !== "FAIL") {
		userToken = token;
		userName = username;
		updateScreen();
	} else {
		alert("Cannot create account.");
	}
}

function search(user) {
	var posts;
	if(user === "") {
		posts = sendRequest("/get-posts", {query: "SELECT * FROM Posts ORDER BY id LIMIT 5"});
	} else {
		posts = sendRequest("/get-posts", {query: `SELECT * FROM Posts WHERE username='${user}' ORDER BY id LIMIT 5`});
	}
	createPosts(posts);
}

function sendPost(text) {
	sendRequest("/new-post", {username: userName, token: userToken, text: text});
	search(document.getElementById('search').value);
}

// Display functions
const makeAccountElem = document.getElementById("make-account");
const newPostElem = document.getElementById("new-post");

function updateScreen() {
	if(userToken === null) {
		makeAccountElem.style.display = "block";
		newPostElem.style.display = "none";
	} else {
		makeAccountElem.style.display = "none";
		newPostElem.style.display = "block";
	}
}

function createPosts(posts) {
	postsElem.innerHTML = "";
	for(let post of posts) {
		var elem = document.createElement("div");

		var text = document.createElement("p");
		text.innerHTML = post.text;
		elem.appendChild(text);

		var author = document.createElement("p");
		author.classList.add("author");
		author.innerHTML = post.username;
		elem.appendChild(author);

		postsElem.appendChild(elem);
	}
}

updateScreen();
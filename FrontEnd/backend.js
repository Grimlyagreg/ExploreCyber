const loggedInUsers = {};

endpoint("/login", data => {
	var req = database.exec(`SELECT password FROM Users WHERE username='${data.username}';`);
	if(req.length > 0 && req[0].values.length === 1) {
		var user = req[0];
		if(user.values[0][0] === data.password) {
			var userToken = randomString();
			loggedInUsers[data.username] = userToken;
			return userToken;
		}
	}
	return "FAIL";
});

endpoint("/signup", data => {
	var req = database.exec(`SELECT password FROM Users WHERE username='${data.username}';`);
	if(req.length === 0 || req[0].values.length === 0) {
		database.run(`INSERT INTO Users (username, password) VALUES ('${data.username}', '${data.password}');`);
		
		var userToken = randomString();
		loggedInUsers[data.username] = userToken;
		return userToken;
	}

	return "FAIL";
});

endpoint("/get-posts", data => {
	var posts = database.exec(data.query)[0];
	var objs = [];
	for(let row of posts.values) {
		var obj = {};
		for(let idx in posts.columns) {
			obj[posts.columns[idx]] = row[idx];
		}
		objs.push(obj);
	}
	return objs;
});

endpoint("/new-post", data => {
	if(loggedInUsers[data.username] === data.token && text !== "") {
		database.run(`INSERT INTO Posts (username, text) VALUES ('${data.username}', '${data.text}');`)
	}
});
const endpoints = {};
var requests = 0;
var functioning = true;
var database;

window.initSqlJs({
	// Required to load the wasm binary asynchronously. Of course, you can host it wherever you want
	// You can omit locateFile completely when running in node
	locateFile: file => `https://sql.js.org/dist/${file}`
}).then(SQL => {
	database = new SQL.Database();
	database.run("CREATE TABLE Users (username VARCHAR(100) PRIMARY KEY, password VARCHAR(100) NOT NULL);\
		CREATE TABLE Posts (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(100) NOT NULL, text VARCHAR(200) NOT NULL);\
		INSERT INTO Users (username, password) VALUES ('admin', 'admin123'), ('alice', 'roses'), ('bob', 'bobcats');");
});

function endpoint(name, callback) {
	endpoints[name] = callback;
}

function sendRequest(endpoint, data) {
	if(!functioning) {
		alert("Website no longer functional.");
	}

	requests++;
	setTimeout(() => requests--, 1000);
	if(requests > 10) {
		functioning = false;
	}
	return endpoints[endpoint](data);
}

function randomString() {
	return Math.random().toString(36).substring(2);
}
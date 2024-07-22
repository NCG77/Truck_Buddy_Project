const express = require("express");
const path = require("path");
const fs = require("fs");
const csv = require("csv-parser");

const app = express();
const usersFilePath = path.join(__dirname, 'users.csv');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Function to read users from CSV file
function readUsers() {
    return new Promise((resolve, reject) => {
        const users = [];
        fs.createReadStream(usersFilePath)
            .pipe(csv())
            .on('data', (row) => {
                users.push(row);
            })
            .on('end', () => {
                resolve(users);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

// Function to write users to CSV file
function writeUsers(users) {
    const headers = "name,email,password\n";
    const userString = users.map(user => `${user.name},${user.email},${user.password}`).join('\n');
    fs.writeFileSync(usersFilePath, headers + userString, 'utf8');
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/signup', async (req, res) => {
    const { name, email, password } = req.body;

    try {
        const users = await readUsers();
        const existingUser = users.find(user => user.name === name);
        if (existingUser) {
            return res.status(400).send("User details already exist");
        }

        const newUser = { name, email, password };
        users.push(newUser);
        writeUsers(users);

        res.redirect("main.html"); 
    } catch (error) {
        console.error(error);
        res.status(500).send("Error registering user");
    }
});

app.post('/login', async (req, res) => {
    const { name, password } = req.body;

    try {
        const users = await readUsers();
        const user = users.find(user => user.name === name && user.password === password);
        if (user) {
            res.redirect("main.html"); 
        } else {
            res.status(400).send("Incorrect username or password");
        }
    } catch (error) {
        console.error(error);
        res.status(500).send("Error logging in");
    }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log("Server is running on port", port);
});

app.post('/signup', async (req, res) => {
    console.log('Signup request received', req.body);
    const { name, email, password } = req.body;

    try {
        const users = await readUsers();
        console.log('Users read from CSV:', users);
        const existingUser = users.find(user => user.name === name);
        if (existingUser) {
            console.log('User already exists');
            return res.status(400).send("User details already exist");
        }

        const newUser = { name, email, password };
        users.push(newUser);
        writeUsers(users);

        res.redirect("/main.html"); // Redirect to main.html after successful registration
    } catch (error) {
        console.error('Error during signup:', error);
        res.status(500).send("Error registering user");
    }
});

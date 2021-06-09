import express from "express";
import fs from "fs";
import path from "path";
import child_process from "child_process";
import cors from "cors";

const app = express();

const corsOpts = {
    origin: "*",
    methods: [
        "GET", "POST"
    ],
    allowedHeaders: [
        "Content-Type"
    ]
};

app.use(cors(corsOpts));

const recentFileName = path.resolve(__dirname, "..", "server_images", "recent.jpg");
const fireFileName = path.resolve(__dirname, "..", "..", "catapult", "catapult.py");

app.listen(3000, () => console.log("Listening at http://localhost:3000"));

app.use(express.static("public"));

app.get("/get-image", (_, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Credentials', "*");

    if (fs.existsSync(recentFileName)) {
        fs.readFile(recentFileName, { encoding: "base64" }, (err, data) => {
            if (err === null) {
                res.send(data);
                fs.renameSync(recentFileName, recentFileName + new Date().toISOString());
            }
        });
    }
    else res.send({ errCode: 120 });
});

app.post("/send-shoot", (_, res) => {
    const firingScript = child_process.spawn("python", [ fireFileName ]);
    res.sendStatus(200);
});

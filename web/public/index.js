const milliseconds = 5000;

const axiosInstance = axios.create({
    baseURL: "",
    timeout: 1000
});

const noMessagesDiv = document.getElementById("noMessagesDiv");
const messagesDiv = document.getElementById("messagesDiv");

const picture = document.getElementById("picture");

function perform() {
    axiosInstance.get("get-image")
        .then((res) => {
            picture.src = "";

            if (res.data.hasOwnProperty("errCode") && res.data.errCode === 120) {
                console.log("No new image.");

                noMessagesDiv.hidden = false;
                messagesDiv.hidden = true;
            } else {
                picture.src = "data:image/jpeg;base64," + res.data;

                noMessagesDiv.hidden = true;
                messagesDiv.hidden = false;

                toggleChecking();
            }
        }).catch((error) => console.log(error));
}

let isPaused = false;
let checkingInterval = setInterval(perform, milliseconds);

function toggleChecking() {
    if (isPaused) {
        checkingInterval = setInterval(perform, milliseconds);
        isPaused = false;
    } else {
        clearInterval(checkingInterval);
        isPaused = true;
    }
}

let shootButton = document.getElementById("shootButton");
let noShootButton = document.getElementById("noShootButton");

shootButton.onclick = () => {
    sendShoot();

    toggleChecking();
};

noShootButton.onclick = () => {
    noMessagesDiv.hidden = false;
    messagesDiv.hidden = true;

    toggleChecking();
};

function sendShoot() {
    axiosInstance.post("send-shoot")
        .then((res) => {
            noMessagesDiv.hidden = false;
            messagesDiv.hidden = true;
        }).catch((err) => console.log(err));
}

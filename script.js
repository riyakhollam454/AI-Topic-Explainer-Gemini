const chatContainer =
    document.getElementById(
        "chat-container"
    );

const messageInput =
    document.getElementById(
        "message"
    );

const sendButton =
    document.getElementById(
        "send-button"
    );


function removeWelcome() {

    const welcome =
        document.querySelector(
            ".welcome"
        );

    if (welcome) {

        welcome.remove();

    }

}


function addMessage(
    message,
    sender
) {

    removeWelcome();

    const messageDiv =
        document.createElement(
            "div"
        );

    messageDiv.className =
        "message " +
        (sender === "user"
            ? "user-message"
            : "bot-message");


    const avatar =
        document.createElement(
            "div"
        );

    avatar.className =
        "avatar " +
        (sender === "user"
            ? "user-avatar"
            : "bot-avatar");


    avatar.innerText =
        sender === "user"
            ? "YOU"
            : "AI";


    const content =
        document.createElement(
            "div"
        );

    content.className =
        "message-content";


    content.innerHTML =
        formatText(message);


    messageDiv.appendChild(
        avatar
    );

    messageDiv.appendChild(
        content
    );

    chatContainer.appendChild(
        messageDiv
    );


    chatContainer.scrollTop =
        chatContainer.scrollHeight;

}


function formatText(text) {

    return text
        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        )
        .replace(
            /\n/g,
            "<br>"
        );

}


function showLoading() {

    const loading =
        document.createElement(
            "div"
        );

    loading.id =
        "loading-message";

    loading.className =
        "message bot-message";


    loading.innerHTML = `

        <div class="avatar bot-avatar">
            AI
        </div>

        <div class="message-content">
            Thinking...
        </div>

    `;


    chatContainer.appendChild(
        loading
    );


    chatContainer.scrollTop =
        chatContainer.scrollHeight;

}


function removeLoading() {

    const loading =
        document.getElementById(
            "loading-message"
        );

    if (loading) {

        loading.remove();

    }

}


async function sendMessage() {

    const question =
        messageInput.value.trim();


    if (!question) {

        return;

    }


    addMessage(
        question,
        "user"
    );


    messageInput.value = "";


    showLoading();


    sendButton.disabled = true;


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: question
                    })
                }
            );


        const data =
            await response.json();


        removeLoading();


        if (data.error) {

            addMessage(
                "Error: " +
                data.error,
                "bot"
            );

        }

        else {

            addMessage(
                data.answer,
                "bot"
            );

        }


    }

    catch (error) {

        removeLoading();

        addMessage(
            "Sorry, something went wrong while connecting to the server.",
            "bot"
        );

        console.error(error);

    }


    sendButton.disabled = false;

    messageInput.focus();

}


function askQuestion(question) {

    messageInput.value =
        question;

    sendMessage();

}


function handleKey(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


function clearChat() {

    chatContainer.innerHTML = `

        <div class="welcome">

            <div class="welcome-icon">
                ✦
            </div>

            <h2>
                What would you like to learn?
            </h2>

            <p>
                Ask me anything from your
                Data Science and GenAI study material.
            </p>

            <div class="suggestions">

                <button onclick="askQuestion(
                    'What is Data Science?'
                )">
                    What is Data Science?
                </button>

                <button onclick="askQuestion(
                    'Explain machine learning'
                )">
                    Explain Machine Learning
                </button>

                <button onclick="askQuestion(
                    'What is RAG?'
                )">
                    What is RAG?
                </button>

                <button onclick="askQuestion(
                    'Explain prompt engineering'
                )">
                    Prompt Engineering
                </button>

            </div>

        </div>

    `;

}
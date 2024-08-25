<script>
  export let peer;
  export let connection;
  export let messagesData;
  export let username;

  import { afterUpdate } from "svelte";
  import Guesswho from "./Guesswho/index.svelte";
  import { images } from "./lib/images.js";

  const colors = ["gray", "green", "blue", "red"];
  const playgroundStatuses = ["chat", "guesswho"];

  let userIDs = ["", peer.id];

  let chatElement;
  let isChatOpen = false;
  let playgroundStatus = "chat";
  let newMessage = "";
  let messages = [
    {
      id: "",
      type: "chat",
      user: "room",
      message: `Connected to: ${connection.peer}`,
      timestamp: new Date().getTime(),
    },
  ];

  const handleChatCommands = (message) => {
    if (message.startsWith("!play")) {
      let action = message.split(" ")[1];
      if (playgroundStatuses.includes(action)) {
        playgroundStatus = action;
      } else {
        console.log("Invalid playground action:", action);
      }
    }
  };

  const toggleChat = () => {
    isChatOpen = !isChatOpen;
  };

  const sendMessage = () => {
    if (newMessage.trim() !== "") {
      messagesData = [
        ...messagesData,
        {
          type: "chat",
          user: "Me",
          id: peer.id,
          message: newMessage,
          timestamp: new Date().getTime(),
        },
      ];
      newMessage = "";
    }
  };

  const addDebugMessage = (msg) => {
    messages = [
      ...messages,
      {
        id: "",
        type: "chat",
        timestamp: new Date().getTime(),
        user: "room",
        message: msg,
      },
    ];
  };

  const handleNewMessage = (message) => {
    console.log("New message:", message);
    // add username
    if (message.id === peer.id) {
      message.user = username;
    }
    // do logic for different message types
    if (message.type === "chat") {
      handleChatCommands(message.message);
      messages = [...messages, message];
    } else {
      console.log("Unknown message type:", message.type);

      if (message.type === "action") {
        if (message.subType === "guesswho") {
          if (message.action === "guess") {
            addDebugMessage(
              `${message.user} guesses character ${images[message.value].name}: ${message.result}`
            );
          } else if (message.action === "question") {
            addDebugMessage(
              `${message.user} asks if the ${message.key} of X is ${message.value}: ${message.result}`
            );
          }
        }
      }
    }
    // send message if we are the source
    if (message.id === peer.id) {
      console.log("Sending message:", message);
      connection.send(JSON.stringify(message));
    }
  };

  afterUpdate(() => {
    scrollToBottom(chatElement);
  });

  const scrollToBottom = async (node) => {
    node.scroll({ top: node.scrollHeight, behavior: "smooth" });
  };

  $: userIDs = ["", peer.id, connection.peer];
  $: messagesData.length &&
    handleNewMessage(messagesData[messagesData.length - 1]);
</script>

<div class="container">
  <!-- Central Content Area -->
  <div class="content">
    {#if playgroundStatus === "chat"}
      <h1>Welcome to the Playground</h1>
      <p>You can chat, but there is also much more!</p>
    {:else if playgroundStatus === "guesswho"}
      <Guesswho bind:peer bind:messagesData />
    {/if}
  </div>
  <!-- Lateral Chat Area -->
  <div class="chat" class:open={isChatOpen}>
    <div class="chat-header">
      <h2>Chat</h2>
    </div>
    <div class="chat-messages" bind:this={chatElement}>
      {#each messages as message}
        <p
          style={`margin-${message.id === peer.id ? "left" : "right"}:${message.id === "" ? 0 : 10}px`}
        >
          {new Date(message.timestamp).toLocaleTimeString("it-IT")} -
          <b
            style={`color:${colors[userIDs.indexOf(message.id) % colors.length]}`}
          >
            {message.user}:
          </b>
          {message.message}
        </p>
      {/each}
    </div>
    <div class="chat-input">
      <input
        type="text"
        placeholder="Type a message..."
        bind:value={newMessage}
        on:keydown={(e) => e.key === "Enter" && sendMessage()}
      />
      <button on:click={sendMessage} class="send-btn">
        &#10148; <!-- Unicode arrow icon for sending -->
      </button>
    </div>
  </div>
</div>

<!-- Button to open chat on small screens -->
<button on:click={toggleChat} class="open-chat-btn" aria-label="Open Chat"
  >💬</button
>

<style>
  .container {
    display: flex;
    min-height: 100vh;
    flex-direction: row;
  }

  .content {
    flex: 1;
    margin-left: 300px;
    padding: 20px;
    background-color: #f4f4f4;
    box-sizing: border-box;
  }

  .chat {
    width: 300px;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    border-right: 1px solid #ccc;
    background-color: #eaeaea;
    box-sizing: border-box;
    transform: translateX(0);
    transition: transform 0.3s ease-in-out;
    display: flex;
    flex-direction: column;
    z-index: 1000;
  }

  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 10px;
    background-color: #ccc;
    border-bottom: 1px solid #bbb;
  }

  .chat-messages p {
    margin: 5px 0;
    padding: 5px;
    background-color: #f1f1f1;
    border-radius: 4px;
    max-width: 100%;
    word-wrap: break-word; /* Ensures long words break to the next line */
    font-size: 10pt;
  }

  .chat-messages {
    text-align: left;
    flex: 1;
    padding: 5px;
    overflow-y: auto; /* Make the messages scrollable */
  }

  .chat-input {
    display: flex;
    padding: 10px;
    border-top: 1px solid #ccc;
    background-color: #f1f1f1;
  }

  .chat-input input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .chat-input button {
    margin-left: 10px;
    padding: 8px 12px;
    background-color: #008cba;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .chat-input button:hover {
    background-color: #007baa;
  }

  .open-chat-btn {
    display: none;
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px;
    font-size: 24px;
    border: none;
    background-color: #008cba;
    color: white;
    border-radius: 50%;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
    z-index: 1000;
  }

  .chat-input button.send-btn {
    margin-left: 10px;
    padding: 8px 12px;
    background-color: #008cba;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 18px; /* Adjust font size for the icon */
  }

  .chat-input button.send-btn:hover {
    background-color: #007baa;
  }

  .chat-input button.send-btn:focus {
    outline: none; /* Remove focus outline */
  }

  @media (max-width: 768px) {
    .container {
      flex-direction: column;
    }

    .chat {
      width: 80%;
      max-width: 320px;
      transform: translateX(-100%);
      z-index: 100;
    }

    .chat.open {
      transform: translateX(0);
    }

    .content {
      margin-left: 0;
    }

    .open-chat-btn {
      display: block;
    }
  }
</style>

<script>
  export let peer;
  export let connection;
  export let status;
  export let messagesData;
  export let username;

  const steps = [
    { id: 0, description: "Enter your username." },
    { id: 1, description: "Choose 'Host' or 'Guest'." },
    { id: 2, description: "Share/Enter the ID" },
  ];

  
  let hostOrGuest = ""; // Can be "host", "guest", or ""
  let currentStep = 0;
  let otherPeerId = "";

  console.log("Peer:", peer);

  const handleData = (data) => {
    console.log("Recived data from peer. Data:", data);
    messagesData = [...messagesData, JSON.parse(data)];
  };

  const bindDataHandle = () => {
    connection.on("data", handleData);
  };

  peer &&
    peer.on("connection", (newConnection) => {
      console.log("New connection");
      if (hostOrGuest === "host") {
        // Allow only a single connection
        if (connection && connection.open) {
          newConnection.on("open", () => {
            newConnection.send("Already connected to another client");
            setTimeout(() => {
              newConnection.close();
            }, 500);
          });
          return;
        }

        connection = newConnection;
        console.log("Connected to: " + connection.peer);
        bindDataHandle();
        status = "connected";
      } else if (hostOrGuest === "guest") {
        // Disallow incoming connections
        newConnection.on("open", () => {
          newConnection.send("Guest does not accept incoming connections");
          setTimeout(() => {
            newConnection.close();
          }, 500);
        });
      } else {
        console.log("Not ready: have not chosen host or guest yet");
      }
    });

  const join = () => {
    status = "connecting";
    // Close old connection
    if (connection) {
      connection.close();
    }

    // Create connection to destination peer specified in the input field
    connection = peer.connect(otherPeerId, { reliable: true });

    // Set up the connection handlers
    connection.on("open", () => {
      status = "connected";
      console.log("Connected to: " + connection.peer);
    });
    bindDataHandle();
    connection.on("close", () => {
      status = "closed";
    });
  };

  $: if (username === "") {
    hostOrGuest = "";
    currentStep = 0;
  } else if (hostOrGuest === "") {
    currentStep = 1;
  } else {
    currentStep = 2;
  }
</script>

<div class="container">
  <h1>Peer to peer communication in JavaScript</h1>
  <h4>Follow these simple steps to get started:</h4>
  <ul>
    {#each steps as { id, description }}
      <li class:completed={currentStep > id} class:current={currentStep === id}>
        <span class="step-label">Step {id + 1}: {description}</span>
      </li>
    {/each}
  </ul>
  <div style="margin-bottom:20px">
    <input
      type="text"
      placeholder="Enter your username"
      bind:value={username}
    />
  </div>
  <div class="buttons">
    {#if peer}
      <button
        class="button host"
        on:click={() => (hostOrGuest = "host")}
        class:filled={hostOrGuest === "host"}
        class:outlined={hostOrGuest !== "host" && hostOrGuest !== "guest"}
        disabled={username === ""}
      >
        Be a Host
      </button>
      <button
        class="button guest"
        on:click={() => (hostOrGuest = "guest")}
        class:filled={hostOrGuest === "guest"}
        class:outlined={hostOrGuest !== "guest" && hostOrGuest !== "host"}
        disabled={username === ""}
      >
        Be a Guest
      </button>
    {:else}
      <p>Wait few seconds, connecting to the server...</p>
    {/if}
  </div>

  {#if hostOrGuest === "host"}
    <h3>You have chosen to be a Host</h3>
    <p>Share the following ID with the Guest:</p>
    <p style="font-weight:bold;font-family:monospace">{peer.id}</p>
    <p>Awaiting connection...</p>
  {/if}
  {#if hostOrGuest === "guest"}
    <h3>You have chosen to be a Guest</h3>
    <p>Connect to the Host with the following ID</p>
    <input
      style="margin-bottom:20px"
      type="text"
      placeholder="Enter the Host ID"
      bind:value={otherPeerId}
    />
    {#if status === "connecting"}
      <p>Connecting...</p>
    {:else}
      <button
        class="button"
        style="color:white;background-color:green"
        disabled={otherPeerId.length < 36}
        on:click={join}
      >
        Connect!
      </button>
    {/if}
  {/if}
</div>

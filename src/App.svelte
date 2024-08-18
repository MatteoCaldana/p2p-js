<script>
  import Peer from "peerjs";
  import Homepage from "./Homepage.svelte";
  import Mainpage from "./Mainpage.svelte";

  let peer = null;
  let lastPeerId = null;
  let connection = null;
  let status = "idle";
  let messagesData = [];
  let username = "";

  const initializePeer = () => {
    peer = new Peer(null, { debug: 2 });

    peer.on("open", (id) => {
      // Workaround for peer.reconnect deleting previous id
      if (peer.id === null) {
        console.log("Received null id from peer open");
        peer.id = lastPeerId;
      } else {
        lastPeerId = peer.id;
      }
      console.log("Peer ID: " + peer.id);
    });

    peer.on("disconnected", function () {
      status = "disconnected";
      console.log("Connection lost.");

      // Workaround for peer.reconnect deleting previous id
      peer.id = lastPeerId;
      peer._lastServerId = lastPeerId;
      peer.reconnect();
    });
    peer.on("close", () => {
      console.log("Connection destroyed");
      status = "closed";
    });
    peer.on("error", (err) => {
      console.log("Error:", err);
      status = "error";
    });
  };
  initializePeer();
</script>

<main>
  {#if status === "error"}
    <p>Peer Error! Please refresh the page.</p>
  {:else if status === "closed"}
    <p>Connection closed! Please refresh the page.</p>
  {:else if status === "disconnected"}
    <p>Peer has disconnected. Trying to reconnect.</p>
  {:else if status === "connected"}
    <Mainpage
      bind:peer
      bind:status
      bind:connection
      bind:messagesData
      bind:username
    />
  {:else}
    <Homepage
      bind:peer
      bind:status
      bind:connection
      bind:messagesData
      bind:username
    />
  {/if}

  <div class="build-timestamp">
    Deployed on: 2024-08-18 12:06:36
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #333;
  }

  .build-timestamp {
    position: fixed;
    bottom: 2px;
    right: 2px;
    font-size: 8px;
    color: #aaa;
  }
</style>

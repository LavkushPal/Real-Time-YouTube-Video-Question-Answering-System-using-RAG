import { useState, useRef, useEffect } from "react";
import axios from "axios";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello👋 how i can help you ?", sender: "other" },
    // { id: 2, text: "Hi! How are you?", sender: "me" },
  ]);

  const [input, setInput] = useState("");
  const [active_url, setActive_url] = useState("");
  const [isQueryHit, setIsQueryHit] = useState(false);

  const bottomRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendVideoToBackend = async (videoId) => {
    try {
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/process-transcript",
        {
          activeUrl: videoId,
        },
      );

      console.log("Response:", data);

      let newMessage = {
        id: Date.now(),
        text: "Ask any question about video",
        sender: "other",
      };

      setMessages((prev) => [...prev, newMessage]);
    } catch (error) {
      console.error("Error:", error.response?.data || error.message);
    }
  };

  function checkIfYouTubeVideo(url) {
    try {
      const parsedUrl = new URL(url);

      const isYouTube = parsedUrl.hostname.includes("youtube.com");
      const isWatchPage = parsedUrl.pathname === "/watch";
      const videoId = parsedUrl.searchParams.get("v");

      if (isYouTube && isWatchPage && videoId) {
        console.log("This is a YouTube video page");
        console.log("Video ID:", videoId);
      } else {
        console.log("Not a youtube video page : please play any youtube video");
      }
    } catch (error) {
      console.log("Invalid URL: please play any youtube video");

      let newMessage = {
        id: Date.now(),
        text: "Invalid URL: please play any youtube video",
        sender: "other",
      };

      setMessages((prev) => [...prev, newMessage]);
    }
  }

  function getActiveTabURL() {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const activeTab = tabs[0];
      if (!activeTab || !activeTab.url) return;

      const url = activeTab.url;

      checkIfYouTubeVideo(url);

      setActive_url(url);
      sendVideoToBackend(url); // send immediately

      setIsQueryHit(false);
    });
  }

  useEffect(() => {
    const init = async () => {
      setIsQueryHit(true);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          text: "Processing transcript....",
          sender: "other",
        },
      ]);

      await getActiveTabURL(); // call backend inside it

    };

    init();
  }, []);

  const processs_query = async (query) => {
    try {
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/process-query",
        {
          query: query
        },
      );

      console.log("Response:", data);

      return data;
    } catch (error) {
      console.error("Error:", error?.data || error.message);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    setIsQueryHit(true);

    const userMessage = {
      id: Date.now(),
      text: input,
      sender: "me",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    const data = await processs_query(input);

    const botMessage = {
      id: Date.now(),
      text: data?.output || "No response",
      sender: "other",
    };

    setMessages((prev) => [...prev, botMessage]);

    setIsQueryHit(false);
  };

  return (
    <div className="flex flex-col  w-[300px] h-[400px] bg-gray-100">
      {/* Header */}
      <div className="p-1 bg-white flex justify-start shadow">
        <h2 className="text-lg font-bold">TubeTalk</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex bg-white ${
              msg.sender === "me" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-xl max-w-xs ${
                msg.sender === "me"
                  ? "bg-blue-500 text-white"
                  : "bg-white text-gray-800"
              }`}
            >
              <p> {msg.text} </p>
              
            </div>
          </div>
        ))}

        {/* Auto scroll target */}
        <div ref={bottomRef}></div>
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t flex gap-2">
        <input
          className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask any question..."
        />
        <button
          onClick={sendMessage}
          disabled={isQueryHit}
          className="bg-blue-500 text-black px-4 py-2 rounded-lg"
        >
          {isQueryHit ? "Wait" : "Send"}
        </button>
      </div>
    </div>
  );
}

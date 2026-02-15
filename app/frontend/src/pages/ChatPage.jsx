import { useState, useRef, useEffect } from "react";
import axios from "axios";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello👋 how i can help you ?", sender: "other" },
    // { id: 2, text: "Hi! How are you?", sender: "me" },
  ]);

  const [input, setInput] = useState("");
  const [active_url,setActive_url]=useState("");

  const bottomRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);


    
    const sendVideoToBackend = async (videoId) => {
    try {
        const response = await axios.post( 
            "http://localhost:5000/api/process-video",
        {
            activeUrl: videoId
        }
        );

        console.log("Response:", response.data);

        newMessage = {
            id: Date.now(),
            text: "Congrats, you can ask question now",
            sender: "other",
        };

        setMessages([...messages, newMessage]);

    } catch (error) {
        console.error("Error:", error.response?.data || error.message);
    }
    };


    useEffect(()=>{
        let newMessage = {
            id: Date.now(),
            text: "Hold on, we are processing video",
            sender: "other",
        };

        setMessages([...messages, newMessage]);

        sendVideoToBackend(active_url);

    },[active_url]);


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
    }
}



  function getActiveTabURL() {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const activeTab = tabs[0];

        if (!activeTab || !activeTab.url) return;

        const url = activeTab.url;
        console.log("Active URL:", url);

        checkIfYouTubeVideo(url);

        setActive_url(url);
    });
}


  useEffect(()=>{
    //fetch youtube url on change in tab activity from current active tab
    //send to backend to do indexing on this video
    
    // getActiveTabURL();

  },[]);

    const processs_query = async (query) => {
    try {
        const response = await axios.post(
        "http://localhost:5000/api/process-query",
        {
            message:"process query ",
            query:query
        }
        );

        console.log("Response:", response.data);

        return response;

    } catch (error) {
        console.error("Error:", error.response?.data || error.message);
    }
    };

  const sendMessage = () => {
    if (!input.trim()) return;

    const newMessage = {
      id: Date.now(),
      text: input,
      sender: "me",
    };

    setMessages([...messages, newMessage]);
    setInput("");

    // const response = processs_query(input);

    // const ewMessage = {
    //   id: Date.now(),
    //   text:response.data?.output,
    //   sender: "other",
    // };

    // setMessages([...messages, ewMessage]);
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
              {msg.text}
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
          className="bg-blue-00 text-black px-4 py-2 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
}

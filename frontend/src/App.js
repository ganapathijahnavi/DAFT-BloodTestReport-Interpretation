// import React, { useState, useRef, useEffect } from "react";
// import { v4 as uuidv4 } from "uuid";

// const App = () => {
//   const [sessions, setSessions] = useState([]);
//   const [activeSessionId, setActiveSessionId] = useState(null);
//   const [selectedFile, setSelectedFile] = useState(null);
//   const [darkMode, setDarkMode] = useState(false);
//   const [loading, setLoading] = useState(false);

//   const fileInputRef = useRef(null);
//   const chatEndRef = useRef(null);

//   const activeSession = sessions.find(s => s.id === activeSessionId);

//   useEffect(() => {
//     chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [activeSession?.messages, loading]);

//   /* ---------- SESSION ---------- */
//   const createNewSession = () => {
//     const id = uuidv4();
//     setSessions(prev => [
//       { id, title: "New Medical Chat", messages: [] },
//       ...prev,
//     ]);
//     setActiveSessionId(id);
//     setSelectedFile(null);
//   };

//   /* ---------- FILE SELECT ---------- */
//   const handleFileSelect = (e) => {
//     const file = e.target.files[0];
//     if (!file) return;

//     if (!activeSessionId) createNewSession();

//     setSelectedFile(file);

//     setSessions(prev =>
//       prev.map(s =>
//         s.id === activeSessionId
//           ? {
//               ...s,
//               messages: [
//                 ...s.messages,
//                 { sender: "user", text: `📎 Attached: ${file.name}` },
//               ],
//             }
//           : s
//       )
//     );
//   };

//   /* ---------- SEND ---------- */
//   const handleSend = async () => {
//     if (!selectedFile || !activeSessionId) return;

//     const formData = new FormData();
//     formData.append("file", selectedFile);

//     setLoading(true);

//     try {
//       const res = await fetch("http://127.0.0.1:8000/upload-ocr", {
//         method: "POST",
//         body: formData,
//       });

//       const data = await res.json();
//       if (!res.ok) throw new Error(data.detail || "Analysis failed");

//       setSessions(prev =>
//         prev.map(s =>
//           s.id === activeSessionId
//             ? {
//                 ...s,
//                 title:
//                   s.title === "New Medical Chat"
//                     ? selectedFile.name.slice(0, 25)
//                     : s.title,
//                 messages: [
//                   ...s.messages,
//                   {
//                     sender: "bot",
//                     title: "🩺 Medical Model Output",
//                     text: data.output || "No output generated.",
//                   },
//                 ],
//               }
//             : s
//         )
//       );
//     } catch (err) {
//       setSessions(prev =>
//         prev.map(s =>
//           s.id === activeSessionId
//             ? {
//                 ...s,
//                 messages: [
//                   ...s.messages,
//                   { sender: "bot", text: `❌ ${err.message}` },
//                 ],
//               }
//             : s
//         )
//       );
//     }

//     setSelectedFile(null);
//     setLoading(false);
//   };

//   const theme = darkMode ? dark : light;

//   return (
//     <div style={{ ...styles.page, background: theme.page }}>
//       {/* SIDEBAR */}
//       <div style={{ ...styles.sidebar, background: theme.sidebar }}>
//         <h2 style={{ color: theme.text }}>🧠 Medical AI</h2>

//         <button style={styles.newChat} onClick={createNewSession}>
//           + New Chat
//         </button>

//         {sessions.map(s => (
//           <div
//             key={s.id}
//             onClick={() => setActiveSessionId(s.id)}
//             style={{
//               ...styles.session,
//               background:
//                 s.id === activeSessionId
//                   ? theme.activeSession
//                   : theme.session,
//               color: theme.text,
//             }}
//           >
//             {s.title}
//           </div>
//         ))}

//         <button style={styles.toggle} onClick={() => setDarkMode(!darkMode)}>
//           {darkMode ? "☀️ Light" : "🌙 Dark"}
//         </button>
//       </div>

//       {/* CHAT */}
//       <div style={{ ...styles.chat, background: theme.chat }}>
//         <div style={styles.messages}>
//           {!activeSession && (
//             <p style={{ color: theme.subText }}>
//               Upload a medical PDF to begin 📄
//             </p>
//           )}

//           {activeSession?.messages.map((m, i) => (
//             <div
//               key={i}
//               style={{
//                 ...styles.message,
//                 alignSelf: m.sender === "user" ? "flex-end" : "flex-start",
//                 background:
//                   m.sender === "user"
//                     ? theme.userBubble
//                     : theme.botBubble,
//                 color: theme.text,
//               }}
//             >
//               {m.title && <strong>{m.title}</strong>}
//               <pre style={styles.pre}>{m.text}</pre>
//             </div>
//           ))}

//           {loading && (
//             <div style={{ ...styles.message, background: theme.botBubble }}>
//               ⏳ Analyzing PDF...
//             </div>
//           )}

//           <div ref={chatEndRef} />
//         </div>

//         {/* INPUT BAR */}
//         <div style={{ ...styles.inputBar, background: theme.input }}>
//           <button
//             style={styles.plus}
//             onClick={() => fileInputRef.current.click()}
//           >
//             +
//           </button>

//           <input
//             ref={fileInputRef}
//             type="file"
//             accept=".pdf"
//             hidden
//             onChange={handleFileSelect}
//           />

//           <input
//             disabled
//             placeholder={
//               selectedFile
//                 ? "PDF attached — click Send"
//                 : "Attach a medical PDF..."
//             }
//             style={styles.input}
//           />

//           <button
//             style={{
//               ...styles.send,
//               opacity: selectedFile ? 1 : 0.4,
//             }}
//             onClick={handleSend}
//             disabled={!selectedFile || loading}
//           >
//             ➜
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// /* THEMES */
// const light = {
//   page: "#eef2ff",
//   sidebar: "#ffffff",
//   chat: "#f9fafb",
//   input: "#ffffff",
//   userBubble: "#2563eb",
//   botBubble: "#e5e7eb",
//   session: "#f3f4f6",
//   activeSession: "#dbeafe",
//   text: "#000",
//   subText: "#6b7280",
// };

// const dark = {
//   page: "#020617",
//   sidebar: "#020617",
//   chat: "#020617",
//   input: "#020617",
//   userBubble: "#2563eb",
//   botBubble: "#1e293b",
//   session: "#020617",
//   activeSession: "#1e293b",
//   text: "#f8fafc",
//   subText: "#94a3b8",
// };

// /* STYLES */
// const styles = {
//   page: { height: "100vh", display: "flex", fontFamily: "Inter" },
//   sidebar: { width: 260, padding: 16 },
//   newChat: {
//     width: "100%",
//     padding: 10,
//     borderRadius: 8,
//     background: "#2563eb",
//     color: "#fff",
//     border: "none",
//     marginBottom: 12,
//   },
//   session: {
//     padding: 10,
//     borderRadius: 8,
//     marginBottom: 6,
//     cursor: "pointer",
//   },
//   toggle: { marginTop: 12, width: "100%", padding: 8 },
//   chat: { flex: 1, display: "flex", flexDirection: "column" },
//   messages: { flex: 1, padding: 16, overflowY: "auto" },
//   message: {
//     maxWidth: "75%",
//     padding: 12,
//     borderRadius: 14,
//     marginBottom: 10,
//   },
//   pre: { margin: 0, whiteSpace: "pre-wrap" },
//   inputBar: { display: "flex", padding: 12, gap: 10 },
//   plus: {
//     width: 40,
//     height: 40,
//     borderRadius: "50%",
//     background: "#2563eb",
//     color: "#fff",
//     fontSize: 22,
//     border: "none",
//   },
//   input: {
//     flex: 1,
//     borderRadius: 999,
//     padding: "10px 14px",
//     border: "1px solid #475569",
//     background: "transparent",
//   },
//   send: {
//     width: 40,
//     height: 40,
//     borderRadius: "50%",
//     background: "#2563eb",
//     color: "#fff",
//     border: "none",
//     fontSize: 20,
//   },
// };

// export default App;

import React, { useState, useRef, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

// Deployed backend base URL (Hugging Face Space)
const API_URL = "https://ganapati-jahnavi-daft-bloodtest-interpretation.hf.space";

const App = () => {
  // Auth state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState("login"); // 'login' or 'signup'
  
  // Form state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [authError, setAuthError] = useState("");
  
  // Chat state
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [speakingIndex, setSpeakingIndex] = useState(null);
  
  // History state
  const [testHistory, setTestHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  
  // Conversational chat state
  const [currentTestId, setCurrentTestId] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const activeSession = sessions.find(s => s.id === activeSessionId);
  
  // Check for stored token on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    
    if (token && storedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(storedUser));
      loadTestHistory();
    }
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeSession?.messages, loading]);

  /* ---------- AUTH FUNCTIONS ---------- */
  const handleAuth = async (e) => {
    e.preventDefault();
    setAuthError("");
    setLoading(true);

    const endpoint = authMode === "login" ? "/auth/login" : "/auth/signup";
    const payload = authMode === "login"
      ? { email, password }
      : { email, password, full_name: fullName };

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || "Authentication failed");
      }

      if (authMode === "signup") {
        // After signup, switch to login mode with success message
        setAuthMode("login");
        setAuthError("");
        setEmail("");
        setPassword("");
        setFullName("");
        alert("✅ Account created successfully! Please login with your credentials.");
      } else {
        // Login: Store token and user
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        
        setIsAuthenticated(true);
        setUser(data.user);
        setEmail("");
        setPassword("");
        
        loadTestHistory();
      }
    } catch (err) {
      setAuthError(err.message);
    }
    
    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setIsAuthenticated(false);
    setUser(null);
    setSessions([]);
    setTestHistory([]);
  };

  /* ---------- TEST HISTORY ---------- */
  const loadTestHistory = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await fetch(`${API_URL}/test-results`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      
      if (res.ok) {
        const data = await res.json();
        setTestHistory(data.results || []);
      }
    } catch (err) {
      console.error("Failed to load history:", err);
    }
  };

  const loadHistoryItem = (item) => {
    const id = uuidv4();
    const newSession = {
      id,
      title: item.file_name.slice(0, 25),
      messages: [
        { sender: "user", text: `📎 ${item.file_name}`, timestamp: new Date(item.uploaded_at) },
        {
          sender: "bot",
          title: "🩺 Medical Model Output",
          text: item.medical_interpretation,
          timestamp: new Date(item.uploaded_at)
        },
      ],
    };
    
    setSessions(prev => [newSession, ...prev]);
    setActiveSessionId(id);
    setShowHistory(false);
  };

  const deleteSession = (sessionId) => {
    setSessions(prev => prev.filter(s => s.id !== sessionId));
    if (activeSessionId === sessionId) {
      setActiveSessionId(null);
    }
  };

  /* ---------- SESSION ---------- */
  const createNewSession = () => {
    const id = uuidv4();
    setSessions(prev => [
      { id, title: "New Medical Chat", messages: [], createdAt: new Date() },
      ...prev,
    ]);
    setActiveSessionId(id);
    setSelectedFile(null);
  };

  /* ---------- FILE SELECT ---------- */
  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!activeSessionId) createNewSession();
    setSelectedFile(file);
  };

  /* ---------- SEND ---------- */
  const handleSend = async () => {
    if (!selectedFile || !activeSessionId) return;

    const userTimestamp = new Date();
    setSessions(prev =>
      prev.map(s =>
        s.id === activeSessionId
          ? {
              ...s,
              messages: [
                ...s.messages,
                { sender: "user", text: `📎 ${selectedFile.name}`, timestamp: userTimestamp },
              ],
            }
          : s
      )
    );

    const formData = new FormData();
    formData.append("file", selectedFile);
    setLoading(true);

    try {
      const token = localStorage.getItem("token");
      
      const res = await fetch(`${API_URL}/upload-ocr`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Analysis failed");

      const botTimestamp = new Date();
      setSessions(prev =>
        prev.map(s =>
          s.id === activeSessionId
            ? {
                ...s,
                title:
                  s.title === "New Medical Chat"
                    ? selectedFile.name.slice(0, 25)
                    : s.title,
                testResultId: data.test_result_id, // Store test result ID
                messages: [
                  ...s.messages,
                  {
                    sender: "bot",
                    title: "🩺 Medical Model Output",
                    text: data.output || "No output generated.",
                    timestamp: botTimestamp
                  },
                ],
              }
            : s
        )
      );
      
      // Set current test ID for chat
      setCurrentTestId(data.test_result_id);
      
      // Reload history to include new test
      loadTestHistory();
    } catch (err) {
      setSessions(prev =>
        prev.map(s =>
          s.id === activeSessionId
            ? {
                ...s,
                messages: [
                  ...s.messages,
                  { sender: "bot", text: `❌ ${err.message}`, timestamp: new Date() },
                ],
              }
            : s
        )
      );
    }

    setSelectedFile(null);
    setLoading(false);
  };

  /* ---------- COPY ---------- */
  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 1500);
  };

  /* ---------- VOICE OUTPUT ---------- */
  const handleSpeak = (text, index) => {
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 0.95;
    utterance.onend = () => setSpeakingIndex(null);

    setSpeakingIndex(index);
    window.speechSynthesis.speak(utterance);
  };

  const handleStop = () => {
    window.speechSynthesis.cancel();
    setSpeakingIndex(null);
  };

  /* ---------- CHAT WITH REPORT ---------- */
  const handleChatMessage = async () => {
    if (!chatInput.trim() || !activeSession?.testResultId) return;

    const userTimestamp = new Date();
    const userMessage = chatInput;
    
    // Add user message to chat
    setSessions(prev =>
      prev.map(s =>
        s.id === activeSessionId
          ? {
              ...s,
              messages: [
                ...s.messages,
                { sender: "user", text: userMessage, timestamp: userTimestamp },
              ],
            }
          : s
      )
    );

    setChatInput("");
    setChatLoading(true);

    try {
      const token = localStorage.getItem("token");
      
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          test_result_id: activeSession.testResultId,
          message: userMessage
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Chat failed");

      const botTimestamp = new Date(); // Use local time instead of server time
      setSessions(prev =>
        prev.map(s =>
          s.id === activeSessionId
            ? {
                ...s,
                messages: [
                  ...s.messages,
                  {
                    sender: "bot",
                    text: data.answer,
                    timestamp: botTimestamp
                  },
                ],
              }
            : s
        )
      );
    } catch (err) {
      setSessions(prev =>
        prev.map(s =>
          s.id === activeSessionId
            ? {
                ...s,
                messages: [
                  ...s.messages,
                  { sender: "bot", text: `❌ ${err.message}`, timestamp: new Date() },
                ],
              }
            : s
        )
      );
    }

    setChatLoading(false);
  };

  const theme = darkMode ? dark : light;

  // If not authenticated, show login/signup form
  if (!isAuthenticated) {
    return (
      <div style={styles.authPage}>
        <div style={styles.authGlow1} />
        <div style={styles.authGlow2} />
        <div style={styles.authCard}>
          <div style={styles.heroPane}>
            <img
              src="https://cdni.iconscout.com/illustration/premium/thumb/login-illustration-svg-download-png-8333958.png"
              alt="Medical lab workspace"
              style={styles.heroImage}
            />
            <div style={styles.heroOverlay}>
              <div style={styles.heroBadge}>Blood Test Insights</div>
              <h2 style={styles.heroTitle}>Upload your report, get clear answers</h2>
              <p style={styles.heroSubtitle}>
                Simple, secure, and fast. Interpret your bloodwork and chat with context-aware explanations.
              </p>
            </div>
          </div>

          <div style={styles.authFormPanel}>
            <div style={styles.authTabs}>
              <button
                style={{
                  ...styles.authTab,
                  ...(authMode === "login" ? styles.authTabActive : {}),
                }}
                onClick={() => {
                  setAuthMode("login");
                  setAuthError("");
                }}
              >
                Login
              </button>
              <button
                style={{
                  ...styles.authTab,
                  ...(authMode === "signup" ? styles.authTabActive : {}),
                }}
                onClick={() => {
                  setAuthMode("signup");
                  setAuthError("");
                }}
              >
                Sign Up
              </button>
            </div>

            <form onSubmit={handleAuth} style={styles.authForm}>
              {authMode === "signup" && (
                <div style={styles.authInputWrap}>
                  <label style={styles.authInputLabel}>Full Name</label>
                  <input
                    type="text"
                    placeholder="Jane Doe"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    style={styles.authInput}
                    required
                  />
                </div>
              )}

              <div style={styles.authInputWrap}>
                <label style={styles.authInputLabel}>Email</label>
                <input
                  type="email"
                  placeholder="you@gmail.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={styles.authInput}
                  required
                />
              </div>

              <div style={styles.authInputWrap}>
                <label style={styles.authInputLabel}>Password</label>
                <input
                  type="password"
                  placeholder="At least 6 characters"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={styles.authInput}
                  required
                  minLength={6}
                />
              </div>

              {authError && <p style={styles.authError}>{authError}</p>}

              <button
                type="submit"
                style={styles.authButton}
                disabled={loading}
              >
                {loading ? "Please wait..." : authMode === "login" ? "Login" : "Create account"}
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ ...styles.page, background: theme.page }}>
      {/* SIDEBAR */}
      <div style={{ ...styles.sidebar, background: theme.sidebar }}>
        <div style={styles.header}>
          <div style={styles.headerIcon}>🧬</div>
          <div>
            <h1 style={styles.headerTitle}>Medical AI</h1>
            <p style={styles.headerSubtitle}>
              Welcome, {user?.full_name?.split(" ")[0]}
            </p>
          </div>
        </div>

        <button style={styles.newChat} onClick={createNewSession}>
          + New Chat
        </button>
        
        <button 
          style={{...styles.historyBtn, background: showHistory ? "#2563eb" : "#475569"}} 
          onClick={() => setShowHistory(!showHistory)}
        >
          📊 Test History ({testHistory.length})
        </button>

        {showHistory ? (
          <div style={styles.historyList}>
            {testHistory.length === 0 ? (
              <p style={{color: theme.subText, fontSize: 12}}>No tests yet</p>
            ) : (
              testHistory.map((item) => (
                <div
                  key={item._id}
                  style={styles.historyItem}
                  onClick={() => loadHistoryItem(item)}
                >
                  <div style={{fontSize: 12, fontWeight: 600}}>{item.file_name}</div>
                  <div style={{fontSize: 10, color: theme.subText}}>
                    {(() => {
                      const date = new Date(item.uploaded_at);
                      const day = String(date.getDate()).padStart(2, '0');
                      const month = String(date.getMonth() + 1).padStart(2, '0');
                      const year = date.getFullYear();
                      return `${day}-${month}-${year}`;
                    })()}
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          sessions.map(s => (
            <div
              key={s.id}
              style={{
                ...styles.session,
                background:
                  s.id === activeSessionId
                    ? theme.activeSession
                    : theme.session,
                color: theme.text,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <div 
                onClick={() => setActiveSessionId(s.id)}
                style={{flex: 1}}
              >
                {s.title}
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteSession(s.id);
                }}
                style={styles.deleteBtn}
                title="Delete chat"
              >
                🗑️
              </button>
            </div>
          ))
        )}

        <div style={{marginTop: "auto"}}>
          <button style={styles.toggle} onClick={() => setDarkMode(!darkMode)}>
            {darkMode ? "☀️ Light" : "🌙 Dark"}
          </button>
          <button style={styles.logoutBtn} onClick={handleLogout}>
            🚪 Logout
          </button>
        </div>
      </div>

      {/* CHAT */}
      <div style={{ ...styles.chat, background: theme.chat }}>
        <div style={styles.messages}>
          {!activeSession && (
            <p style={{ color: theme.subText }}>
              Upload a medical PDF to begin 📄
            </p>
          )}

          {activeSession?.messages.map((m, i) => (
            <div
              key={i}
              style={{
                ...styles.message,
                alignSelf: m.sender === "user" ? "flex-end" : "flex-start",
                background:
                  m.sender === "user"
                    ? theme.userBubble
                    : theme.botBubble,
                color: theme.text,
                position: "relative",
              }}
            >
              {m.title && <strong>{m.title}</strong>}
              <pre style={styles.pre}>{m.text}</pre>
              
              {/* Timestamp */}
              {m.timestamp && (
                <div style={styles.timestamp}>
                  {(() => {
                    const date = new Date(m.timestamp);
                    const hours = String(date.getHours()).padStart(2, '0');
                    const minutes = String(date.getMinutes()).padStart(2, '0');
                    return `${hours}:${minutes}`;
                  })()}
                </div>
              )}

              {m.sender === "bot" && (
                <div style={styles.actionRow}>
                  <button
                    style={styles.copyBtn}
                    onClick={() => handleCopy(m.text, i)}
                  >
                    {copiedIndex === i ? "✓ Copied" : "📋 Copy"}
                  </button>

                  {speakingIndex === i ? (
                    <button style={styles.voiceBtn} onClick={handleStop}>
                      ⏹ Stop
                    </button>
                  ) : (
                    <button
                      style={styles.voiceBtn}
                      onClick={() => handleSpeak(m.text, i)}
                    >
                      🔊 Speak
                    </button>
                  )}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div style={{ ...styles.message, background: theme.botBubble, color: theme.text }}>
              <div style={styles.loadingContainer}>
                <div style={styles.loadingSpinner}>⏳</div>
                <div>
                  <strong>Analyzing your medical report...</strong>
                  <div style={styles.loadingSubtext}>
                    • Extracting text with OCR<br/>
                    • Parsing lab values<br/>
                    • Running AI medical interpretation<br/>
                    <br/>
                    <em>⏱️ This typically takes 1-2 minutes. Please wait...</em>
                  </div>
                </div>
              </div>
            </div>
          )}

          {chatLoading && (
            <div style={{ ...styles.message, background: theme.botBubble, color: theme.text }}>
              <div style={styles.loadingContainer}>
                <div style={styles.loadingSpinner}>⏳</div>
                <div>
                  <strong>Thinking...</strong>
                </div>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {selectedFile && (
          <div style={styles.filePreview}>
            📄 {selectedFile.name}
            <span
              style={styles.removeFile}
              onClick={() => setSelectedFile(null)}
            >
              ✕
            </span>
          </div>
        )}

        <div style={{ ...styles.inputBar, background: theme.input }}>
          {!activeSession?.testResultId ? (
            // File upload mode
            <>
              <button
                style={styles.plus}
                onClick={() => fileInputRef.current.click()}
              >
                +
              </button>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                hidden
                onChange={handleFileSelect}
              />

              <input
                disabled
                placeholder={
                  selectedFile
                    ? "PDF attached — press Enter or Send"
                    : "Attach a medical PDF..."
                }
                style={styles.input}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && selectedFile && !loading) {
                    handleSend();
                  }
                }}
              />

              <button
                style={{
                  ...styles.send,
                  opacity: selectedFile ? 1 : 0.4,
                }}
                onClick={handleSend}
                disabled={!selectedFile || loading}
              >
                ➜
              </button>
            </>
          ) : (
            // Chat mode (after report is analyzed)
            <>
              <button
                style={styles.plus}
                onClick={() => fileInputRef.current.click()}
                title="Upload new report"
              >
                📄
              </button>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                hidden
                onChange={handleFileSelect}
              />

              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask a question about this report..."
                style={styles.input}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && chatInput.trim() && !chatLoading) {
                    handleChatMessage();
                  }
                }}
              />

              <button
                style={{
                  ...styles.send,
                  opacity: chatInput.trim() ? 1 : 0.4,
                }}
                onClick={handleChatMessage}
                disabled={!chatInput.trim() || chatLoading}
              >
                ➜
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

/* THEMES */
const light = {
  page: "#eef2ff",
  sidebar: "#ffffff",
  chat: "#f9fafb",
  input: "#ffffff",
  userBubble: "#2563eb",
  botBubble: "#e5e7eb",
  session: "#f3f4f6",
  activeSession: "#dbeafe",
  text: "#000",
  subText: "#6b7280",
};

const dark = {
  page: "#020617",
  sidebar: "#020617",
  chat: "#020617",
  input: "#020617",
  userBubble: "#2563eb",
  botBubble: "#1e293b",
  session: "#020617",
  activeSession: "#1e293b",
  text: "#f8fafc",
  subText: "#94a3b8",
};

/* STYLES */
const styles = {
  // Auth styles
  authPage: {
    height: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "linear-gradient(135deg, #eef2ff 0%, #dce7ff 50%, #f7f9ff 100%)",
    position: "relative",
    overflow: "hidden",
    padding: 16,
    fontFamily: "Inter",
  },
  authGlow1: {
    position: "absolute",
    width: 500,
    height: 500,
    background: "rgba(255,255,255,0.08)",
    filter: "blur(100px)",
    top: -150,
    left: -150,
    borderRadius: "50%",
    pointerEvents: "none",
  },
  authGlow2: {
    position: "absolute",
    width: 500,
    height: 500,
    background: "rgba(255,255,255,0.08)",
    filter: "blur(100px)",
    bottom: -150,
    right: -150,
    borderRadius: "50%",
    pointerEvents: "none",
  },
  authCard: {
    position: "relative",
    width: "100%",
    maxWidth: 820,
    maxHeight: "90vh",
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 20,
    padding: 20,
    borderRadius: 22,
    background: "rgba(255,255,255,0.98)",
    border: "1px solid rgba(255,255,255,0.3)",
    boxShadow: "0 24px 70px rgba(0,0,0,0.14)",
    backdropFilter: "blur(16px)",
    overflow: "hidden",
  },
  heroPane: {
    position: "relative",
    borderRadius: 16,
    overflow: "hidden",
    minHeight: 280,
    maxHeight: "80vh",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
  },
  heroImage: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    display: "block",
    filter: "saturate(1.05)",
  },
  heroOverlay: {
    position: "absolute",
    inset: 0,
    background: "linear-gradient(180deg, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.75) 100%)",
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
    gap: 8,
    padding: 18,
    color: "#fff",
  },
  heroBadge: {
    display: "inline-flex",
    padding: "8px 12px",
    borderRadius: 999,
    background: "rgba(255,255,255,0.14)",
    color: "#ffffff",
    fontWeight: 700,
    fontSize: 12,
    width: "fit-content",
    border: "1px solid rgba(255,255,255,0.2)",
  },
  heroTitle: {
    margin: 0,
    fontSize: 26,
    lineHeight: 1.25,
    fontWeight: 800,
    color: "#ffffff",
  },
  heroSubtitle: {
    margin: 0,
    fontSize: 14,
    color: "#e2e8f0",
    lineHeight: 1.55,
    maxWidth: 520,
  },
  authFormPanel: {
    background: "#ffffff",
    borderRadius: 22,
    padding: 20,
    border: "1px solid rgba(255,255,255,0.3)",
    boxShadow: "0 20px 50px rgba(0,0,0,0.15)",
    display: "flex",
    flexDirection: "column",
    maxHeight: "80vh",
    overflowY: "auto",
  },
  formHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 10,
  },
  formBadge: {
    display: "inline-flex",
    padding: "6px 10px",
    borderRadius: 10,
    background: "rgba(37,99,235,0.12)",
    color: "#1d4ed8",
    fontWeight: 700,
    fontSize: 12,
    marginBottom: 6,
  },
  formSubline: {
    fontSize: 13,
    color: "#475569",
  },
  formSecurity: {
    fontSize: 12,
    color: "#0f172a",
    fontWeight: 700,
    background: "rgba(34,197,94,0.12)",
    padding: "8px 12px",
    borderRadius: 12,
    border: "1px solid rgba(34,197,94,0.2)",
  },
  authTabs: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 12,
    marginBottom: 14,
  },
  authTab: {
    padding: 12,
    borderRadius: 12,
    background: "#f8fafc",
    border: "1px solid rgba(226,232,240,0.9)",
    color: "#0f172a",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: 14,
    transition: "all 0.2s ease",
  },
  authTabActive: {
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    color: "#fff",
    border: "1px solid rgba(102,126,234,0.5)",
    boxShadow: "0 8px 20px rgba(102,126,234,0.3)",
  },
  authForm: {
    display: "flex",
    flexDirection: "column",
    gap: 14,
  },
  authInputWrap: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
  },
  authInputLabel: {
    fontSize: 12,
    color: "#94a3b8",
    letterSpacing: 0.2,
    textTransform: "uppercase",
  },
  authInput: {
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid #e2e8f0",
    background: "#ffffff",
    color: "#0f172a",
    fontSize: 14,
    outline: "none",
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
  },
  authButton: {
    padding: 14,
    borderRadius: 12,
    border: "none",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    color: "#fff",
    fontSize: 15.5,
    fontWeight: 700,
    cursor: "pointer",
    boxShadow: "0 8px 20px rgba(102,126,234,0.3)",
  },
  authError: {
    color: "#fca5a5",
    fontSize: 13,
    margin: 0,
  },
  authFooterRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: 12,
    marginTop: 6,
    color: "#475569",
    fontSize: 12,
  },
  authHint: {
    opacity: 0.95,
  },
  authLink: {
    color: "#7c3aed",
    cursor: "pointer",
    textDecoration: "none",
    fontWeight: 600,
  },
  
  // Main app styles
  page: { height: "100vh", display: "flex", fontFamily: "Inter" },
  sidebar: { width: 260, padding: 16, display: "flex", flexDirection: "column" },

  header: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    padding: "14px 12px",
    borderRadius: 14,
    marginBottom: 18,
    background: "linear-gradient(135deg, #2563eb, #4f46e5)",
    boxShadow: "0 10px 25px rgba(0,0,0,0.15)",
  },
  headerIcon: {
    width: 46,
    height: 46,
    borderRadius: "50%",
    background: "#ffffff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 22,
  },
  headerTitle: { margin: 0, fontSize: 20, fontWeight: 700, color: "#fff" },
  headerSubtitle: { margin: 0, fontSize: 14, color: "#fff", opacity: 0.95 },

  newChat: {
    width: "100%",
    padding: 10,
    borderRadius: 8,
    background: "#2563eb",
    color: "#fff",
    border: "none",
    marginBottom: 12,
    cursor: "pointer",
  },
  historyBtn: {
    width: "100%",
    padding: 10,
    borderRadius: 8,
    background: "#475569",
    color: "#fff",
    border: "none",
    marginBottom: 12,
    cursor: "pointer",
  },
  historyList: {
    maxHeight: 300,
    overflowY: "auto",
    marginBottom: 12,
  },
  historyItem: {
    padding: 8,
    borderRadius: 6,
    marginBottom: 6,
    background: "#f1f5f9",
    cursor: "pointer",
  },
  session: { padding: 10, borderRadius: 8, marginBottom: 6, cursor: "pointer" },
  deleteBtn: {
    background: "transparent",
    border: "none",
    cursor: "pointer",
    fontSize: 16,
    padding: "4px 8px",
    opacity: 0.7,
  },
  toggle: { width: "100%", padding: 8, marginBottom: 6, cursor: "pointer" },
  logoutBtn: {
    width: "100%",
    padding: 8,
    background: "#dc2626",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
  },

  chat: { flex: 1, display: "flex", flexDirection: "column" },
  messages: { flex: 1, padding: 16, overflowY: "auto" },
  message: {
    maxWidth: "75%",
    padding: 12,
    paddingBottom: 24,
    borderRadius: 14,
    marginBottom: 10,
    position: "relative",
  },
  pre: { margin: 0, whiteSpace: "pre-wrap" },

  timestamp: {
    fontSize: 10,
    opacity: 0.6,
    marginTop: 8,
    fontStyle: "italic",
    textAlign: "right",
    position: "absolute",
    bottom: 6,
    right: 12,
  },

  actionRow: {
    display: "flex",
    gap: 10,
    marginTop: 6,
  },

  copyBtn: {
    fontSize: 12,
    border: "none",
    background: "transparent",
    cursor: "pointer",
    opacity: 0.8,
  },

  voiceBtn: {
    fontSize: 12,
    border: "none",
    background: "transparent",
    cursor: "pointer",
    opacity: 0.8,
  },

  loadingContainer: {
    display: "flex",
    gap: 12,
    alignItems: "flex-start",
  },

  loadingSpinner: {
    fontSize: 24,
    animation: "spin 2s linear infinite",
  },

  loadingSubtext: {
    fontSize: 12,
    marginTop: 8,
    opacity: 0.9,
    lineHeight: 1.6,
  },

  inputBar: { display: "flex", padding: 12, gap: 10 },
  plus: {
    width: 40,
    height: 40,
    borderRadius: "50%",
    background: "#2563eb",
    color: "#fff",
    fontSize: 22,
    border: "none",
    cursor: "pointer",
  },
  input: {
    flex: 1,
    borderRadius: 999,
    padding: "10px 14px",
    border: "1px solid #475569",
    background: "transparent",
  },
  send: {
    width: 40,
    height: 40,
    borderRadius: "50%",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    fontSize: 20,
    cursor: "pointer",
  },
  filePreview: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "8px 12px",
    margin: "0 12px 6px",
    borderRadius: 10,
    background: "#e5e7eb",
    fontSize: 14,
  },
  removeFile: { cursor: "pointer", fontWeight: "bold" },
};

export default App;

import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);
  const [history, setHistory] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  const BACKEND_URL = "https://structurai.onrender.com";

  const generate = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setErrorMessage(""); // reset old error

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000);

      const res = await fetch(`${BACKEND_URL}/generate-ui`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      let data = {};
      try {
        data = await res.json();
      } catch {
        throw new Error("Invalid response from server.");
      }

      if (!res.ok || data.error) {
        throw new Error(data.detail || data.error || "Server error occurred.");
      }

      const relativePath = data.preview_url || data.url;

      if (!relativePath || typeof relativePath !== "string") {
        throw new Error("Backend did not return a valid preview URL.");
      }

      const fullPreviewUrl = relativePath.startsWith("http")
        ? relativePath
        : `${BACKEND_URL}${relativePath.startsWith("/") ? "" : "/"}${relativePath}`;

      setPreview(fullPreviewUrl);
      setHasGenerated(true);

      const newVersion = {
        id: Date.now(),
        prompt,
        url: fullPreviewUrl,
        version: history.length + 1
      };

      setHistory([newVersion, ...history]);

    } catch (err) {
      console.error("Design generation failed:", err);

      if (err.name === "AbortError") {
        setErrorMessage("Server is waking up. Please wait 30–60 seconds and try again.");
      } else {
        setErrorMessage(err.message || "Something went wrong.");
      }

    } finally {
      setLoading(false);
    }
  };

  const switchVersion = (item) => {
    setPrompt(item.prompt);
    setPreview(item.url);
  };

  // Hero Section
  if (!hasGenerated) {
    return (
      <div style={styles.heroPage}>
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>StructurAI <span style={styles.accent}>Studio</span></h1>
          <p style={styles.heroSubtitle}>Transform thoughts into interfaces instantly.</p>

          {errorMessage && (  
            <div style={styles.errorBox}>{errorMessage}</div>
          )}

          <div style={styles.heroCard}>
            <textarea 
              style={styles.heroTextarea} 
              placeholder="Describe your UI (e.g., 'A modern SaaS dashboard for a crypto app')..." 
              value={prompt} 
              onChange={(e) => setPrompt(e.target.value)} 
            />
            <button style={styles.mainButton} onClick={generate} disabled={loading}>
              {loading ? "Designing..." : "Generate UI"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Workspace Section
  return (
    <div style={styles.workspace}>
      <aside style={styles.editorSidebar}>
        <div style={styles.sidebarHeader}>
          <div style={styles.logoGroup}>
             <div style={styles.logoBox}>S</div>
             <span style={styles.logoText}>Studio</span>
          </div>
          <button onClick={() => {setHasGenerated(false); setHistory([]);}} style={styles.backBtn}>Reset</button>
        </div>

        {errorMessage && (  
          <div style={styles.errorBox}>{errorMessage}</div>
        )}
        
        <div style={styles.chatArea}>
          <textarea 
            style={styles.sidebarTextarea} 
            value={prompt} 
            onChange={(e) => setPrompt(e.target.value)} 
            placeholder="Ask for changes..."
          />
          <button style={styles.updateButton} onClick={generate} disabled={loading}>
            {loading ? "Refining..." : "Update Design"}
          </button>
        </div>

        <div style={styles.historySection}>
          <h3 style={styles.historyTitle}>Version History</h3>
          <div style={styles.historyList}>
            {history.map((item) => (
              <div 
                key={item.id} 
                style={{
                  ...styles.historyItem,
                  border: preview === item.url ? "1px solid #3b82f6" : "1px solid #222"
                }} 
                onClick={() => switchVersion(item)}
              >
                <div style={styles.versionLabel}>v{item.version}</div>
                <div style={styles.versionPrompt}>{item.prompt.substring(0, 40)}...</div>
              </div>
            ))}
          </div>
        </div>
      </aside>

      <main style={styles.previewArea}>
        <div style={styles.previewHeader}>
          <div style={styles.versionChip}>Live Preview</div>
          <div style={styles.actions}>
             <button style={styles.secondaryBtn} onClick={() => window.open(preview, '_blank')}>Open Fullscreen</button>
             <button style={styles.publishBtn}>Publish</button>
          </div>
        </div>
        <div style={styles.iframeContainer}>
          <iframe 
            src={preview} 
            style={styles.iframe} 
            title="preview" 
            sandbox="allow-scripts allow-same-origin"
          />
        </div>
      </main>
    </div>
  );
}

const styles = {
  ...{
    heroPage: { minHeight: "100vh", background: "#020617", display: "flex", justifyContent: "center", alignItems: "center", color: "white", fontFamily: "Inter, sans-serif" },
    heroContent: { textAlign: "center", width: "100%", maxWidth: "700px", padding: "20px" },
    heroTitle: { fontSize: "4.5rem", fontWeight: "900", margin: 0, letterSpacing: "-2px" },
    accent: { background: "linear-gradient(to right, #3b82f6, #a855f7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" },
    heroSubtitle: { opacity: 0.5, fontSize: "1.2rem", marginBottom: "20px", marginTop: "10px" },
    heroCard: { background: "rgba(255,255,255,0.03)", padding: "30px", borderRadius: "28px", border: "1px solid rgba(255,255,255,0.1)", boxShadow: "0 20px 50px rgba(0,0,0,0.5)" },
    heroTextarea: { width: "100%", height: "140px", background: "transparent", border: "none", color: "white", fontSize: "1.2rem", outline: "none", resize: "none" },
    mainButton: { width: "100%", padding: "18px", borderRadius: "16px", background: "#3b82f6", color: "white", fontWeight: "700", border: "none", cursor: "pointer", marginTop: "20px", fontSize: "1.1rem" },

    errorBox: {   
      background: "rgba(255,0,0,0.1)",
      color: "#ff6b6b",
      padding: "12px",
      borderRadius: "12px",
      marginBottom: "20px",
      fontSize: "14px"
    }
  }
};

export default App;
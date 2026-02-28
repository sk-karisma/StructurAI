import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);
  // NEW: Version History State
  const [history, setHistory] = useState([]);

  const generate = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/generate-ui", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      
      setPreview(data.preview_url);
      setHasGenerated(true);
      
      // Add new generation to history
      const newVersion = {
        id: Date.now(),
        prompt: prompt,
        url: data.preview_url,
        version: history.length + 1
      };
      setHistory([newVersion, ...history]);
      
    } catch (err) {
      console.error("Design generation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const switchVersion = (item) => {
    setPrompt(item.prompt);
    setPreview(item.url);
  };

  if (!hasGenerated) {
    return (
      <div style={styles.heroPage}>
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>StructurAI <span style={styles.accent}>Studio</span></h1>
          <p style={styles.heroSubtitle}>Transform thoughts into interfaces instantly.</p>
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

        {/* NEW: Version History Section */}
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
             <button style={styles.secondaryBtn}>View Code</button>
             <button style={styles.publishBtn}>Publish</button>
          </div>
        </div>
        <div style={styles.iframeContainer}>
          <iframe src={preview} style={styles.iframe} title="preview" />
        </div>
      </main>
    </div>
  );
}

const styles = {
  // ... (previous heroPage, heroContent, etc. styles remain the same)
  heroPage: { minHeight: "100vh", background: "#020617", display: "flex", justifyContent: "center", alignItems: "center", color: "white", fontFamily: "Inter, sans-serif" },
  heroContent: { textAlign: "center", width: "100%", maxWidth: "700px", padding: "20px" },
  heroTitle: { fontSize: "4.5rem", fontWeight: "900", margin: 0, letterSpacing: "-2px" },
  accent: { background: "linear-gradient(to right, #3b82f6, #a855f7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" },
  heroSubtitle: { opacity: 0.5, fontSize: "1.2rem", marginBottom: "40px", marginTop: "10px" },
  heroCard: { background: "rgba(255,255,255,0.03)", padding: "30px", borderRadius: "28px", border: "1px solid rgba(255,255,255,0.1)", boxShadow: "0 20px 50px rgba(0,0,0,0.5)" },
  heroTextarea: { width: "100%", height: "140px", background: "transparent", border: "none", color: "white", fontSize: "1.2rem", outline: "none", resize: "none" },
  mainButton: { width: "100%", padding: "18px", borderRadius: "16px", background: "#3b82f6", color: "white", fontWeight: "700", border: "none", cursor: "pointer", marginTop: "20px", fontSize: "1.1rem" },

  workspace: { display: "flex", height: "100vh", background: "#0a0a0a", color: "white", fontFamily: "Inter, sans-serif" },
  editorSidebar: { width: "380px", borderRight: "1px solid #222", padding: "24px", display: "flex", flexDirection: "column", background: "#0d0d0d" },
  sidebarHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" },
  logoGroup: { display: "flex", alignItems: "center", gap: "10px" },
  logoBox: { width: "32px", height: "32px", background: "#3b82f6", borderRadius: "8px", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold" },
  logoText: { fontWeight: "700", fontSize: "1.2rem" },
  backBtn: { background: "transparent", border: "none", color: "#666", cursor: "pointer", fontSize: "13px" },
  chatArea: { height: "250px", display: "flex", flexDirection: "column", gap: "10px", marginBottom: "30px" },
  sidebarTextarea: { flex: 1, background: "#111", border: "1px solid #333", borderRadius: "16px", padding: "15px", color: "white", resize: "none", outline: "none", fontSize: "14px" },
  updateButton: { padding: "12px", background: "#3b82f6", borderRadius: "12px", border: "none", color: "white", fontWeight: "700", cursor: "pointer" },
  
  // History Styles
  historySection: { flex: 1, display: "flex", flexDirection: "column", overflowY: "auto" },
  historyTitle: { fontSize: "12px", fontWeight: "700", textTransform: "uppercase", color: "#444", marginBottom: "15px", letterSpacing: "1px" },
  historyList: { display: "flex", flexDirection: "column", gap: "10px" },
  historyItem: { padding: "12px", background: "#111", borderRadius: "12px", cursor: "pointer", transition: "all 0.2s" },
  versionLabel: { fontSize: "10px", fontWeight: "800", color: "#3b82f6", marginBottom: "4px" },
  versionPrompt: { fontSize: "12px", color: "#888", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" },

  previewArea: { flex: 1, display: "flex", flexDirection: "column", background: "#f1f5f9" },
  previewHeader: { padding: "12px 24px", background: "#fff", borderBottom: "1px solid #e2e8f0", display: "flex", justifyContent: "space-between", alignItems: "center" },
  versionChip: { background: "#f1f5f9", color: "#64748b", padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" },
  actions: { display: "flex", gap: "10px" },
  secondaryBtn: { background: "transparent", border: "1px solid #e2e8f0", padding: "8px 16px", borderRadius: "8px", fontSize: "13px", fontWeight: "600", cursor: "pointer" },
  publishBtn: { background: "#000", color: "#fff", border: "none", padding: "8px 16px", borderRadius: "8px", fontSize: "13px", fontWeight: "600", cursor: "pointer" },
  iframeContainer: { flex: 1, padding: "20px" },
  iframe: { width: "100%", height: "100%", border: "none", borderRadius: "16px", background: "#fff", boxShadow: "0 10px 30px rgba(0,0,0,0.05)" }
};

export default App;
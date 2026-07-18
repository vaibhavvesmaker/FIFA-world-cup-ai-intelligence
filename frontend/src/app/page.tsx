const pillars = [
  {
    label: "Live intelligence",
    title: "Match pulse",
    description: "Event ingestion, match state, and timestamped probability changes.",
    icon: "◉",
  },
  {
    label: "Historical analytics",
    title: "World Cup archive",
    description: "Explore tournaments, teams, players, lineups, and decisive moments.",
    icon: "⌁",
  },
  {
    label: "Grounded AI",
    title: "Research copilot",
    description: "Structured calculations and cited retrieval—not invented statistics.",
    icon: "✦",
  },
];

const modelSteps = [
  ["01", "Ingest", "Receive and validate match events"],
  ["02", "Predict", "Recalculate win and draw probability"],
  ["03", "Explain", "Identify the features driving change"],
  ["04", "Audit", "Store the prediction with its timestamp"],
];

export default function Home() {
  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="PitchPulse home">
          <span className="brand-mark">P</span>
          <span>
            <strong>PITCHPULSE</strong>
            <small>WORLD CUP AI</small>
          </span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#intelligence">Intelligence</a>
          <a href="#history">History</a>
          <a href="#method">Method</a>
        </nav>
        <div className="system-status">
          <span className="status-dot" /> Foundation online
        </div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <div className="eyebrow">AI-POWERED FOOTBALL INTELLIGENCE</div>
          <h1>
            Every match has a story.
            <span>We make the data explain it.</span>
          </h1>
          <p>
            A real-time World Cup decision engine combining live match data,
            auditable predictions, historical similarity, and cited AI answers.
          </p>
          <div className="hero-actions">
            <a className="primary-button" href="#intelligence">
              Explore the foundation <span>→</span>
            </a>
            <a className="text-button" href="#method">
              See how it works
            </a>
          </div>
        </div>

        <div className="match-console" aria-label="Live intelligence preview">
          <div className="console-head">
            <span>INTELLIGENCE CONSOLE</span>
            <span className="pending-pill">DATA SOURCE PENDING</span>
          </div>
          <div className="console-body">
            <div className="orbital" aria-hidden="true">
              <span className="orbit orbit-one" />
              <span className="orbit orbit-two" />
              <span className="core">AI</span>
            </div>
            <div className="console-message">
              <span className="signal-label">SYSTEM READY</span>
              <h2>Waiting for a verified match feed</h2>
              <p>
                The interface will never present staged data as live. Source,
                freshness, and model version will appear with every prediction.
              </p>
            </div>
          </div>
          <div className="console-foot">
            <span>API <b>READY</b></span>
            <span>MODEL <b>STAGING</b></span>
            <span>RAG <b>PLANNED</b></span>
          </div>
        </div>
      </section>

      <section className="proof-strip" aria-label="System principles">
        <div><strong>TRACEABLE</strong><span>Every prediction timestamped</span></div>
        <div><strong>GROUNDED</strong><span>Answers tied to evidence</span></div>
        <div><strong>REAL-TIME</strong><span>Freshness made visible</span></div>
        <div><strong>AUDITABLE</strong><span>Models evaluated after play</span></div>
      </section>

      <section className="section" id="intelligence">
        <div className="section-heading">
          <div>
            <span className="eyebrow">ONE CONNECTED SYSTEM</span>
            <h2>From live event to useful intelligence</h2>
          </div>
          <p>
            The product separates numerical calculation from generative AI, so
            the model can communicate clearly without fabricating the match.
          </p>
        </div>
        <div className="pillar-grid">
          {pillars.map((pillar) => (
            <article className="pillar-card" key={pillar.title}>
              <span className="card-icon">{pillar.icon}</span>
              <small>{pillar.label}</small>
              <h3>{pillar.title}</h3>
              <p>{pillar.description}</p>
              <span className="card-link">Planned capability →</span>
            </article>
          ))}
        </div>
      </section>

      <section className="history-section" id="history">
        <div className="history-copy">
          <span className="eyebrow">HISTORICAL MATCH TWIN</span>
          <h2>Ask the past what could happen next.</h2>
          <p>
            Match Twin will compare the current score, minute, discipline, and
            performance profile with historical World Cup states—then retrieve
            the closest precedents and their outcomes.
          </p>
          <div className="query-example">
            <small>EXAMPLE QUESTION</small>
            <p>“Which knockout matches looked most like this at 65 minutes?”</p>
          </div>
        </div>
        <div className="twin-panel">
          <div className="twin-title">
            <span>SIMILARITY PIPELINE</span><b>DESIGN STAGE</b>
          </div>
          <div className="twin-row"><span>Match-state filters</span><em>SQL</em></div>
          <div className="twin-row"><span>Nearest historical states</span><em>VECTOR</em></div>
          <div className="twin-row"><span>Reports and tournament context</span><em>RAG</em></div>
          <div className="twin-row"><span>Cited natural-language answer</span><em>LLM</em></div>
        </div>
      </section>

      <section className="section method" id="method">
        <div className="section-heading">
          <div>
            <span className="eyebrow">AUDITABLE BY DESIGN</span>
            <h2>The live prediction loop</h2>
          </div>
          <p>
            A prediction is only credible when we can reproduce what the system
            knew at that moment and why its estimate moved.
          </p>
        </div>
        <div className="steps">
          {modelSteps.map(([number, title, description]) => (
            <div className="step" key={number}>
              <span>{number}</span><h3>{title}</h3><p>{description}</p>
            </div>
          ))}
        </div>
      </section>

      <footer>
        <div className="brand footer-brand">
          <span className="brand-mark">P</span>
          <span><strong>PITCHPULSE</strong><small>WORLD CUP AI</small></span>
        </div>
        <p>Foundation milestone · No unverified live data displayed</p>
        <p>Built by Vaibhav Vesmaker</p>
      </footer>
    </main>
  );
}
